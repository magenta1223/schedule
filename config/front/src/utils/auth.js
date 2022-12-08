function setToken() { // header 내용에 토큰 붙여주기
    let token = localStorage.getItem('access_token')
    let config = {
        Authorization : `Bearer ${token}`
    };
    return config
}





export default setToken

