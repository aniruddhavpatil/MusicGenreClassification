const baseUrl = "http://localhost:3011/";

const api = {
    Urls: {
        upload: baseUrl + "upload",
        uploadDone: baseUrl + "video/upload/done",
        reco: baseUrl + "video/reco",
    },

    make: function (url, method, params){
      return fetch(url, {
          method,
          headers:{
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(params),
      }).then(response => response.json());
    },
    post: function (url, params) {
      return this.make(url, 'POST',params);
    },
    get: function (url) {
      return this.make(url, 'GET');
    },
};

export default api;
