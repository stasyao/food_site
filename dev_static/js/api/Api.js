class Api {
  constructor(apiUrl) {
      this.apiUrl =  apiUrl;
  }
getPurchases () {
  return fetch(apiUrl + `/purchases/`, {
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
    }
  })
    .then( e => {
        if(e.ok) {
            return e.json()
        }
        return Promise.reject(e.statusText)
    })
}
addPurchases (id) {
  return fetch(apiUrl + `/purchases/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
    },
    body: JSON.stringify({
      id: id
    })
  })
    .then( e => {
        if(e.ok) {
            return e.json()
        }
        return Promise.reject(e.statusText)
    })
}
removePurchases (id){
  return fetch(apiUrl + `/purchases/${id}/`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
    }
  })
    .then( e => {
        if(e.ok) {
            return e.json()
        }
        return Promise.reject(e.statusText)
    })
}
  addSubscriptions(id) {
    return fetch(apiUrl + `/follow/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
      },
      body: JSON.stringify({
        id: id
      })
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  removeSubscriptions (id) {
    return fetch(apiUrl + `/follow/${id}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
      }
    })
      .then( e => {
          if(e.ok) {
              return e.json()
          }
          return Promise.reject(e.statusText)
      })
  }
  addFavorites (id)  {
    return fetch(apiUrl + `/favorites/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
      },
      body: JSON.stringify({
        id: id
      })
    })
        .then( e => {
            if(e.ok) {
                return e.json()
            }
            return Promise.reject(e.statusText)
        })
  }
  removeFavorites (id) {
    return fetch(apiUrl + `/favorites/${id}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
      }
    })
        .then( e => {
            if(e.ok) {
                return e.json()
            }
            return Promise.reject(e.statusText)
        })
  }
    getIngredients  (text)  {
        return fetch(apiUrl + `/ingredients?search=${text}`, {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
            }
        })
            .then( e => {
                if(e.ok) {
                    return e.json()
                }
                return Promise.reject(e.statusText)
            })
    }
}
