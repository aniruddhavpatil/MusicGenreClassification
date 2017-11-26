import {compose, createStore} from 'redux'
import {persistStore, autoRehydrate} from 'redux-persist'
import reducer from '../reducers/reducer'

// add `autoRehydrate` as an enhancer to your store (note: `autoRehydrate` is not a middleware)
const store = createStore(
  reducer,
  undefined,
  compose(
    autoRehydrate({log: true})
  )
)

// begin periodically persisting the store
persistStore(store)

export default store
