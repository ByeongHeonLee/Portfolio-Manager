//kakao
export const KAKAO_CLIENT_ID = "a595d733fea16f9c91a507688b4a2f0b";
export const KAKAO_REDIRECT_URI = "http://localhost:3000/oauth/callback/kakao";
export const KAKAO_AUTH_URL = `https://kauth.kakao.com/oauth/authorize?client_id=${KAKAO_CLIENT_ID}&redirect_uri=${KAKAO_REDIRECT_URI}&response_type=code`;

//naver
export const NAVER_CLIENT_ID = "iPWtavszxbcjYZ943T0O";
export const NAVER_CLIENT_SECRET = "IYERhyLfSk";
export const NAVER_CALLBACK_URL = "http://localhost:3000/oauth/callback/naver";
export const NAVER_AUTH_URL = `https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=${NAVER_CLIENT_ID}&state=1234567890&redirect_uri=${NAVER_CALLBACK_URL}`;
