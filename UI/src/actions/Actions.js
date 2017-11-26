export function setUser(username){
  return {
    type: 'SET_USER',
    username
  }
}

export function logout(username){
  return {
    type: 'LOGOUT'
  }
}

export function calledLogin(){
  return{
    type: 'LOGIN_SET'
  }
}
