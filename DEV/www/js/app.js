new Vue({

  el: '#app',

  data: {
  	report: []
  },

  mounted() {
  	// make an ajax request and output the data
 	// use axios
 	axios.get('../data/response.json').then(response => this.report = response.data);
 	
  }



});