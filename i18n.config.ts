export default defineI18nConfig(() => ({
  legacy: false,
  locale: "en",
  fallbackLocale: "cn",
  messages: {
    en: {
      welcome: "welcome",
      time: "Current time: ",
      sry1: "Sorry, the prizes are already claimed",
      sry2: "Sorry, you have already participated in this lucky draw",
      thx: "Thank you for your participation",
      scrs: "Do not refresh the page and screenshot your prize record",
      prize: "The prize you won is ",
      won: "Congratulations, you won the ",
      wheel: "Lucky Wheel Lucky Draw",
      user: "The winning user is: ",
    },
    cn: {
      welcome: "欢迎加入",
      time: "当前时间：",
      sry1: "很抱歉，奖品已经被抽完",
      sry2: "很抱歉，你已经参与过该抽奖活动",
      thx: "十分感谢您的参与",
      scrs: "请勿刷新界面并截图以保存获奖记录",
      prize: "抽到的奖品为：",
      won: "恭喜你抽到了 ",
      wheel: "幸运转盘抽奖",
      user: "获奖用户为：",
    },
  },
}));
