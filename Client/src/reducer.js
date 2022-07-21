



export const reducerStore = createStore (combineReducer({dati}),composeEnhancers(applyMiddleware(thunkMiddlware)));

