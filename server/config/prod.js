
// on Heroku
// module.exports = {
//     mongoURI:process.env.MONGO_URI,
//     mongoURI_stock_info:process.env.MONGODB_STOCK_INFO_URI,
//     KAKAO_AUTH_URL:process.env.REACT_APP_KAKAO_REDIRECT_URI,
//     NAVER_CLIENT_ID:process.env.REACT_APP_NAVER_CLIENT_ID,
//     NAVER_CALLBACK_URL:process.env.REACT_APP_NAVER_CALLBACK_URL
// }

// on Local
module.exports = {
    mongoURI:'mongodb+srv://lsh:dltjdgur123@cluster0.5jaze.mongodb.net/myFirstDatabase?retryWrites=true&w=majority',
    mongoURI_stock_info:'mongodb+srv://ByeongHeonLee:portfoliodotcom@portfolio-dot-com.yaba9.mongodb.net/?retryWrites=true&w=majority',
    KAKAO_AUTH_URL:'https://portfolio-dot-com.herokuapp.com/oauth/callback/kakao',
    NAVER_CLIENT_ID:'iPWtavszxbcjYZ943T0O',
    NAVER_CALLBACK_URL:'https://portfolio-dot-com.herokuapp.com/oauth/callback/naver'
}
