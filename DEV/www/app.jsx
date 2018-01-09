Vue.component('rounds-patientlist', {
  template: `
        <table class="table">
          <thead>
            <tr>
              <th><abbr title="PatientID">MRN</abbr></th>
              <th>Name</th>
              <th><abbr title="Age">Age</abbr></th>
              <th><abbr title="LOS">LOS</abbr></th>
              <th><abbr title="Diagnosis">Dx</abbr></th>
              <th><abbr title="Admitted">Admitted</abbr></th>
              <th><abbr title="NIHSS">NIHSS</abbr></th>
              <th><abbr title="NurseReview">NR</abbr></th>
              <th><abbr title="Bed">Bed</abbr></th>
              <th><abbr title="BP">BP</abbr></th>
              <th><abbr title="BSL">BSL</abbr></th>
              <th><abbr title="Temp">T</abbr></th>
              <th><abbr title="SpeechPath">SP</abbr></th>
              <th>Status</th>
            </tr>
          </thead>
          <tfoot>
            <tr>
              <th><abbr title="PatientID">MRN</abbr></th>
              <th>Name</th>
              <th><abbr title="Age">Age</abbr></th>
              <th><abbr title="LOS">LOS</abbr></th>
              <th><abbr title="Diagnosis">Dx</abbr></th>
              <th><abbr title="Admitted">Admitted</abbr></th>
              <th><abbr title="NIHSS">NIHSS</abbr></th>
              <th><abbr title="NurseReview">NR</abbr></th>
              <th><abbr title="Bed">Bed</abbr></th>
              <th><abbr title="BP">BP</abbr></th>
              <th><abbr title="BSL">BSL</abbr></th>
              <th><abbr title="Temp">T</abbr></th>
              <th><abbr title="SpeechPath">SP</abbr></th>
              <th>Status</th>
            </tr>
          </tfoot>
          <tbody>
            <patient-detail></patient-detail>
          </tbody>
        </table>
  `,

});

Vue.component('rounds-list', {
  template: `#patient-list`,
  props: {
    data: Array,
    columns: Array,
    filterKey: String
  },
  data: function () {
    var sortOrders = {}
    this.columns.forEach(function (key) {
      sortOrders[key] = 1
    })
    return {
      sortKey: '',
      sortOrders: sortOrders
    }
  },
  computed: {
    patientList: function () {
      var sortKey = this.sortKey
      var filterKey = this.filterKey && this.filterKey.toLowerCase()
      var order = this.sortOrders[sortKey] || 1
      var data = this.data
      if (filterKey) {
        data = data.filter(function (row) {
          return Object.keys(row).some(function (key) {
            return String(row[key]).toLowerCase().indexOf(filterKey) > -1
          })
        })
      }
      if (sortKey) {
        data = data.slice().sort(function (a, b) {
          a = a[sortKey]
          b = b[sortKey]
          return (a === b ? 0 : a > b ? 1 : -1) * order
        })
      }
      return data
    }
  },
  filters: {
    capitalize: function (str) {
      index = str.indexOf('_')
      console.log('for str ' + str + ' index = ' + index)
      if (index != -1) {
        return str.slice(0, index).toUpperCase() + " " + str.slice(index+1).toUpperCase()
      } else {
        return str.toUpperCase()
      }
    }
  },
  methods: {
    sortBy: function (key) {
      this.sortKey = key
      this.sortOrders[key] = this.sortOrders[key] * -1
    }
  }
})

new Vue({
  el: '#root',
  data: {
  	title: 'Rounds Dashboard',
    searchQuery: '',
    patientList: [],
    gridColumns: ['name', 'mrn', 'age', 'los', 'diagnosis', 'admitted', 'nihss', 'nurse_review', 'bed', 'bp', 'bsl', 'temp', 'speech_path', 'status'],
  	isLoading: false,
  	isDisabled: true
  },

  created() {
    // see laracasts
    axios.get('data/sample.json').then(response => this.patientList = response.data);
  }
})