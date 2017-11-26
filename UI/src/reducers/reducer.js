const initState = {
  username: "",
  rehydrated: false,
  loggedin: false,
}

const reducer = (state = initState,action) => {
  switch(action.type){
    case 'SET_USER':
      return { ...state, username: action.username}
    case 'persist/REHYDRATE':
      let name = action.payload.username
      if(name == undefined){
        name = ''
      }
      return {...state, rehydrated: true, username: name}
    case 'LOGOUT':
      return {...state, username: ''}
    case 'LOGIN_SET':
      return {...state, loggedin: true}
    default:
      return state
  }
}

export default reducer
