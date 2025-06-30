from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    HTTPException,
    Header,
)
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt, re, uvicorn, os

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

# 定义允许跨域访问的源
origins = [
    "*",
]

# 启用CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/api/public", StaticFiles(directory="public"), name="public")


def get_current_user(authorization: Optional[str] = Header(None)):

    if authorization is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # 通常 Authorization 头的格式是 "Bearer <token>"
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    except Exception as e:
        raise HTTPException(
            status_code=401, detail="Invalid authorization header format"
        )

    try:
        payload = decode_access_token(token)
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@app.get("/api_public/{file_path:path}")
async def serve_public_file(
    file_path: str, user: Optional[dict] = Depends(get_current_user)
):
    # 构建完整的文件路径
    full_path = os.path.join("public", file_path)

    # 检查文件是否存在且是文件（不是目录）
    if not os.path.exists(full_path) or not os.path.isfile(full_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(full_path)


# JWT Configuration
SECRET_KEY = "your-secret-key-here"  # Change this to a strong secret in production
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 1

# USER_DATABASE = {
#     "admin": {
#         "username": "admin",
#         "password": "admin123",  # In production, store hashed passwords
#         "role": "admin",
#     },
#     "user": {"username": "user", "password": "user123", "role": "user"},
# }

USER_DATABASE = {
    "admin": {
        "password": "admin123",  # In production, store hashed passwords
        "role": "admin",
    },
    "msbio": {"password": "msbio123", "role": "admin"},
    "user": {"password": "user123", "role": "user"},
}


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    print("JWT:", encoded_jwt)
    print(decode_access_token(encoded_jwt))
    return encoded_jwt


# 任何对Header或Payload的修改都会导致签名验证失败
def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"],
            options={
                "verify_exp": True,  # 验证过期时间
                "verify_signature": True,  # 验证签名 with SECRET_KEY
            },
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError as e:
        raise Exception(f"Invalid token: {str(e)}")
    except Exception as e:
        raise Exception(f"Error decoding token: {str(e)}")


class LoginRequest(BaseModel):
    username: str
    password: str


# @app.post("/login_portal")
# async def login(login_request: LoginRequest):
#     user = USER_DATABASE.get(login_request.username)
#     print(login_request, user)
#     if not user or user["password"] != login_request.password:
#         raise HTTPException(status_code=401, detail="Incorrect username or password")

#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={
#             "sub": login_request.username,
#             "role": user["role"],
#         },
#         expires_delta=access_token_expires,
#     )

#     return {"access_token": access_token, "token_type": "bearer"}


@app.post("/login_portal")
async def login(login_request: LoginRequest):
    try:
        user = USER_DATABASE.get(login_request.username)
        print(login_request, user)
        if not user or user["password"] != login_request.password:
            raise HTTPException(
                status_code=401, detail="Incorrect username or password"
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": login_request.username,
                "role": user["role"],
            },
            expires_delta=access_token_expires,
        )

        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        print(f"Unexpected error during login: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"{str(e)}",
        )


# BioMolecular Function
from enum import Enum
from typing import Optional


class MolarityCalculatorRequest(BaseModel):
    massValue: Optional[float] = None
    massUnit: Optional[str] = None
    concentrationValue: Optional[float] = None
    concentrationUnit: Optional[str] = None
    volumeValue: Optional[float] = None
    volumeUnit: Optional[str] = None
    molecularWeight: float  # 单位默认为 g/mol


class MolarityCalculatorResponse(BaseModel):
    calculatedValue: float
    calculatedUnit: str
    message: str


def convert_to_standard_units(value: float, unit: str, conversion_type: str) -> float:
    """将各种单位转换为标准单位(g, M, L)"""
    if conversion_type == "mass":
        if unit == "mg":
            return value / 1000
        elif unit == "kg":
            return value * 1000
        else:  # g
            return value
    elif conversion_type == "concentration":
        if unit == "fM":
            return value / 1_000_000_000_000
        elif unit == "pM":
            return value / 1_000_000_000
        elif unit == "nM":
            return value / 1_000_000
        elif unit == "μM":
            return value / 1_000_000
        elif unit == "mM":
            return value / 1000
        else:  # M
            return value
    elif conversion_type == "volume":
        if unit == "μL":
            return value / 1_000_000
        elif unit == "mL":
            return value / 1000
        else:  # L
            return value


def get_optimal_unit(value: float, unit_type: str) -> tuple[float, str]:
    """
    根据值的大小选择最合适的单位，并调整值
    返回调整后的值和单位
    """
    if unit_type == "mass":
        if abs(value) >= 1000:
            return value / 1000, "kg"
        elif abs(value) < 0.001:
            return value * 1000, "mg"
        else:
            return value, "g"
    elif unit_type == "concentration":
        abs_value = abs(value)
        if abs_value >= 1:
            return value, "M"
        elif abs_value >= 0.001:
            return value * 1000, "mM"
        elif abs_value >= 1e-6:
            return value * 1_000_000, "μM"
        elif abs_value >= 1e-9:
            return value * 1_000_000_000, "nM"
        elif abs_value >= 1e-12:
            return value * 1_000_000_000_000, "pM"
        else:
            return value * 1_000_000_000_000_000, "fM"
    elif unit_type == "volume":
        if abs(value) >= 1:
            return value, "L"
        elif abs(value) >= 0.001:
            return value * 1000, "mL"
        else:
            return value * 1_000_000, "μL"
    else:
        raise ValueError(f"Unknown unit type: {unit_type}")


@app.post("/molarity_calculator", response_model=MolarityCalculatorResponse)
async def molarity_calculator(request: MolarityCalculatorRequest):
    # 检查参数有效性
    none_count = sum(
        1
        for field in [
            request.massValue,
            request.concentrationValue,
            request.volumeValue,
        ]
        if field is None
    )
    if none_count != 1:
        raise HTTPException(
            status_code=400,
            detail="必须有且只能有一个值为空(massValue, concentrationValue 或 volumeValue)",
        )

    # 将输入值转换为标准单位(g, M, L)
    if request.massValue is not None and request.massUnit is not None:
        mass_std = convert_to_standard_units(
            request.massValue, request.massUnit, "mass"
        )
    if request.concentrationValue is not None and request.concentrationUnit is not None:
        conc_std = convert_to_standard_units(
            request.concentrationValue, request.concentrationUnit, "concentration"
        )
    if request.volumeValue is not None and request.volumeUnit is not None:
        vol_std = convert_to_standard_units(
            request.volumeValue, request.volumeUnit, "volume"
        )

    molecular_weight = request.molecularWeight  # g/mol

    # 根据缺失的值进行计算
    if request.massValue is None:
        # 计算质量: mass = concentration * volume * molecular_weight
        calculated_value_std = conc_std * vol_std * molecular_weight
        calculated_value, optimal_unit = get_optimal_unit(calculated_value_std, "mass")
        return {
            "calculatedValue": float(f"{calculated_value:.4g}"),
            "calculatedUnit": optimal_unit,
            "message": "Calculated mass",
        }

    elif request.concentrationValue is None:
        # 计算浓度: concentration = mass / (volume * molecular_weight)
        calculated_value_std = mass_std / (vol_std * molecular_weight)
        calculated_value, optimal_unit = get_optimal_unit(
            calculated_value_std, "concentration"
        )
        return {
            "calculatedValue": float(f"{calculated_value:.4g}"),
            "calculatedUnit": optimal_unit,
            "message": "Calculated concentration",
        }

    elif request.volumeValue is None:
        # 计算体积: volume = mass / (concentration * molecular_weight)
        calculated_value_std = mass_std / (conc_std * molecular_weight)
        calculated_value, optimal_unit = get_optimal_unit(
            calculated_value_std, "volume"
        )
        return {
            "calculatedValue": float(f"{calculated_value:.4g}"),
            "calculatedUnit": optimal_unit,
            "message": "Calculated volume",
        }

    else:
        raise HTTPException(
            status_code=400,
            detail="必须有一个值为空(massValue, concentrationValue 或 volumeValue)",
        )


@app.post("/mass_calculator")
async def mass_calculator(data: dict):
    # 原子质量表（相对原子质量，基于IUPAC 2013标准）
    ATOMIC_MASS = {
        "H": 1.008,
        "He": 4.0026,
        "Li": 6.94,
        "Be": 9.0122,
        "B": 10.81,
        "C": 12.011,
        "N": 14.007,
        "O": 15.999,
        "F": 18.998,
        "Ne": 20.180,
        "Na": 22.990,
        "Mg": 24.305,
        "Al": 26.982,
        "Si": 28.085,
        "P": 30.974,
        "S": 32.06,
        "Cl": 35.45,
        "Ar": 39.948,
        "K": 39.098,
        "Ca": 40.078,
    }

    try:
        formula = data.get("molecularFormula", "").strip()
        if not formula:
            raise HTTPException(status_code=400, detail="分子式不能为空")

        # 使用正则表达式匹配元素和数量
        pattern = r"([A-Z][a-z]*)(\d*)"
        matches = re.findall(pattern, formula)

        if not matches:
            raise HTTPException(status_code=400, detail="无效的分子式格式")

        total_weight = 0.0

        for element, count in matches:
            if element not in ATOMIC_MASS:
                raise HTTPException(status_code=400, detail=f"未知元素: {element}")

            try:
                atomic_mass = ATOMIC_MASS[element]
                num_atoms = int(count) if count else 1
                total_weight += atomic_mass * num_atoms
            except ValueError:
                raise HTTPException(
                    status_code=400, detail=f"元素 {element} 的数量无效: {count}"
                )

        molecular_weight = round(total_weight, 4)

        return {
            "molecularFormula": formula,
            "molecularWeight": molecular_weight,
            "unit": "g/mol",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"发生错误: {str(e)}")


class DilutionRequest(BaseModel):
    c1Value: Optional[float] = None
    c1Unit: Optional[str] = None
    v1Value: Optional[float] = None
    v1Unit: Optional[str] = None
    c2Value: Optional[float] = None
    c2Unit: Optional[str] = None
    v2Value: Optional[float] = None
    v2Unit: Optional[str] = None


class DilutionResponse(BaseModel):
    calculatedValue: float
    calculatedUnit: str
    message: str


def convert_to_base(value: float, unit: str) -> float:
    """将所有单位转换为基本单位(M和L)"""
    if unit == "mM":
        return value * 1e-3
    elif unit == "μM":
        return value * 1e-6
    elif unit == "nM":
        return value * 1e-9
    elif unit == "pM":
        return value * 1e-12
    elif unit == "fM":
        return value * 1e-15
    elif unit == "mL":
        return value * 1e-3
    elif unit == "μL":
        return value * 1e-6
    else:  # M or L
        return value


def find_optimal_unit(value: float, is_concentration: bool) -> tuple:
    """根据值的大小找到最合适的单位"""
    abs_value = abs(value)

    if is_concentration:
        if abs_value >= 1:
            return value, "M"
        elif abs_value >= 1e-3:
            return value / 1e-3, "mM"
        elif abs_value >= 1e-6:
            return value / 1e-6, "μM"
        elif abs_value >= 1e-9:
            return value / 1e-9, "nM"
        elif abs_value >= 1e-12:
            return value / 1e-12, "pM"
        else:
            return value / 1e-15, "fM"
    else:  # volume
        if abs_value >= 1:
            return value, "L"
        elif abs_value >= 1e-3:
            return value / 1e-3, "mL"
        else:
            return value / 1e-6, "μL"


@app.post("/dilution_calculator", response_model=DilutionResponse)
async def calculate_dilution(request: DilutionRequest):
    # 检查只有一个值为空
    none_count = sum(
        1
        for field in [
            request.c1Value,
            request.v1Value,
            request.c2Value,
            request.v2Value,
        ]
        if field is None
    )
    if none_count != 1:
        return {
            "calculatedValue": 0,
            "calculatedUnit": "",
            "message": "必须有且只有一个值为空(待计算值)",
        }

    # 将所有值转换为基本单位(M和L)
    c1 = (
        convert_to_base(request.c1Value, request.c1Unit)
        if request.c1Value is not None
        else None
    )
    v1 = (
        convert_to_base(request.v1Value, request.v1Unit)
        if request.v1Value is not None
        else None
    )
    c2 = (
        convert_to_base(request.c2Value, request.c2Unit)
        if request.c2Value is not None
        else None
    )
    v2 = (
        convert_to_base(request.v2Value, request.v2Unit)
        if request.v2Value is not None
        else None
    )

    # 根据稀释公式 C1V1 = C2V2 计算缺失的值
    calculated_value = 0.0
    calculated_unit = ""
    message = ""

    if request.c1Value is None:
        # 计算初始浓度 C1 = C2V2/V1
        calculated_value = (c2 * v2) / v1
        optimal_value, optimal_unit = find_optimal_unit(
            calculated_value, is_concentration=True
        )
        calculated_value = float(f"{optimal_value:.4g}")
        calculated_unit = optimal_unit
        message = f"Initial concentration is: {calculated_value} {calculated_unit}"

    elif request.v1Value is None:
        # 计算初始体积 V1 = C2V2/C1
        calculated_value = (c2 * v2) / c1
        optimal_value, optimal_unit = find_optimal_unit(
            calculated_value, is_concentration=False
        )
        calculated_value = float(f"{optimal_value:.4g}")
        calculated_unit = optimal_unit
        message = f"Initial volume is: {calculated_value} {calculated_unit}"

    elif request.c2Value is None:
        # 计算稀释后浓度 C2 = C1V1/V2
        calculated_value = (c1 * v1) / v2
        optimal_value, optimal_unit = find_optimal_unit(
            calculated_value, is_concentration=True
        )
        calculated_value = float(f"{optimal_value:.4g}")
        calculated_unit = optimal_unit
        message = f"Diluted concentration is: {calculated_value} {calculated_unit}"

    elif request.v2Value is None:
        # 计算稀释后体积 V2 = C1V1/C2
        calculated_value = (c1 * v1) / c2
        optimal_value, optimal_unit = find_optimal_unit(
            calculated_value, is_concentration=False
        )
        calculated_value = float(f"{optimal_value:.4g}")
        calculated_unit = optimal_unit
        message = f"Diluted volume is: {calculated_value} {calculated_unit}"

    return {
        "calculatedValue": calculated_value,
        "calculatedUnit": calculated_unit,
        "message": message,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8082, workers=1, reload=True)
