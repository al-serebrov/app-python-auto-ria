<template>
  <div max-width="800px">
    <vue-topprogress ref="topProgress"></vue-topprogress>
    <div>
        Последние поиски:
        <table class="table">
          <thead>
            <tr>
              <th scope="col">Kaтегория</th>
              <th scope="col">Кузов</th>
              <th scope="col">Марка</th>
              <th scope="col">Модель</th>
              <th scope="col">Коробка передач</th>
              <th scope="col">Топливо</th>
              <th scope="col">Цвет</th>
              <th scope="col">Привод</th>
              <th scope="col">Начальный год</th>
              <th scope="col">Конечный год</th>
              <th scope="col">Область</th>
              <th scope="col">Город</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="search in searches" :key="search.id">
              <td>{{ search.category.name }}</td>
              <td>{{ search.bodystyle.name }}</td>
              <td>{{ search.mark.name }}</td>
              <td>{{ search.model.name }}</td>
              <td>{{ search.gear.name }}</td>
              <td>{{ search.fuel.name }}</td>
              <td>{{ search.color.name }}</td>
              <td>{{ search.driver_type.name }}</td>
              <td>{{ search.start_year.name }}</td>
              <td>{{ search.end_year.name }}</td>
              <td>{{ search.state.name }}</td>
              <td>{{ search.city.name }}</td>
              <td><a @click="applySearch(search.id)" href="#">Применить</a></td>
              <td><a @click="deleteSearch(search.id)" href="#">Удалить</a></td>
            </tr>
          </tbody>
        </table> 
    </div>
    Параметры поиска:
    <div class="flex-parent">
      <label class="required flex-child">Категория</label>
      <v-select
        class="flex-child"
        label="name"
        :options="categories"
        v-model="selected.category"
        @input="onCategoryChange"
      />
    </div>
    <div class="flex-parent">
      <label class="flex-child">Кузов</label>
      <v-select
        class="flex-child"
        label="name"
        :options="bodystyles"
        :disabled="bodystyles.length == 0"
        v-model="selected.bodystyle"
      />
    </div>
    <div class="flex-parent">
      <label class="flex-child">Марка</label>
      <v-select
        class="flex-child"
        label="name"
        :options="marks"
        :disabled="marks.length == 0"
        v-model="selected.mark"
        @input="onMarkChange"
      />
    </div>
    <div class="flex-parent">
      <label class="flex-child">Модель</label>
      <v-select
        class="flex-child"
        label="name"
        :options="models"
        :disabled="models.length == 0"
        v-model="selected.model"
      />
    </div>
    <div class="flex-parent">
      <label class="flex-child">Коробка передач</label>
      <v-select
        class="flex-child"
        label="name"
        :options="gears"
        :disabled="gears.length == 0"
        v-model="selected.gear"
      />
    </div>
    <div class="flex-parent">
      <label class="flex-child">Топливо</label>
      <v-select
        class="flex-child"
        label="name"
        :options="fuels"
        :disabled="fuels.length == 0"
        v-model="selected.fuel"
      />
    </div>
    <div class="flex-parent">
      <label class="flex-child">Цвет</label>
      <v-select
        class="flex-child"
        label="name"
        :options="colors"
        v-model="selected.color"
      />
    </div>
    <div class="flex-parent">
      <label class="flex-child">Привод</label>
      <v-select
        class="flex-child"
        label="name"
        :options="driverTypes"
        :disabled="driverTypes.length == 0"
        v-model="selected.driver_type"
      />
    </div>
    <div class="flex-parent">
      <label class="flex-child">Начальный год</label>
      <v-select
        class="flex-child"
        label="name"
        value="value"
        :options="years"
        v-model="selected.start_year"
      />
    </div>
    <div class="flex-parent">
      <label class="flex-child">Конечный год</label>
      <v-select
        class="flex-child"
        label="name"
        value="value"
        :options="years"
        v-model="selected.end_year"
      />
    </div>
    <div class="flex-parent">
      <label class="flex-child">Область</label>
      <v-select
        class="flex-child"
        label="name"
        :options="states"
        v-model="selected.state"
        @input="onStateChange"
      />
    </div>
    <div class="flex-parent">
      <label class="flex-child">Город</label>
      <v-select
        class="flex-child"
        label="name"
        :options="cities"
        :disabled="cities.length == 0"
        v-model="selected.city"
      />
    </div>
      <button v-on:click=calculate>Рассчет средней цены</button>
      <br>
      <div v-if="calculated">
        <p>Всего объявлений: {{ total }}</p>
        <p>Средняя цена: {{ arithmeticMean }}</p>
        <input type="checkbox" v-model="showMore" @change="getMoreInfo"/> Больше информации
        <table class="table">
          <thead>
            <tr>
              <th scope="col">
                Ссылка на <a href="https://auto.ria.com">auto.ria.com</a>
              </th>
              <template v-if="showMore">
                <th scope="col">Модель</th>
                <th scope="col">Город</th>
                <th scope="col">Год выпуска</th>
                <th scope="col">Пробег</th>
              </template>
              <th scope="col">Цена</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in classifiedsLimited" :key="item.id">
              <td><a :href="item.url" target="_blank">{{ item.url }}</a></td>
              <template v-if="showMore">
                <td>{{ item.model }}</td>
                <td>{{ item.city }}</td>
                <td>{{ item.year }}</td>
                <td>{{ item.race }}</td>
              </template>
              <td>{{ item.price }}</td>
            </tr>
          </tbody>
        </table> 
        <button @click="prevPage">Показать меньше</button>
        <button @click="nextPage">Показать больше</button>
      </div>
  </div>
</template>

<style>
.inline-block-child {
  display: inline-block;
}
.flex-parent {
  display: flex;
}
.flex-child {
  flex: 1;
}
.required:after {
    content:" *";
    color: red;
}
</style>

<script>
import axios from 'axios';                                
import { vueTopprogress } from 'vue-top-progress'

const api_url = `http://${process.env.VUE_APP_API_ENDPOINT}:5000`;

export default {
  name: 'Average',
  data() {
    return {
      searches: [],
      categories: [],
      bodystyles: [],
      marks: [],
      models: [],
      gears: [],
      states: [],
      cities: [],
      fuels: [],
      colors: [],
      driverTypes: [],
      years: [],
      average: {},
      classifieds: [],
      classifiedsLimited: [],
      showMore: false,
      calculated: false,
      limit: 10,
      start: 10,
      total: 0,
      arithmeticMean: 0,
      selected: {
          category: {name: null, value: null},
          bodystyle: {name: null, value: null},
          state: {name: null, value: null},
          gear: {name: null,  value: null},
          model: {name: null, value: null},
          mark: {name: null, value: null},
          city: {name: null, value: null},
          fuel: {name: null, value: null},
          color: {name: null, value: null},
          driver_type: {name: null, value: null},
          start_year: {name: null, value: null},
          end_year: {name: null, value: null},
      }
    };
  },
  components: {
    vueTopprogress
  },
  methods: {
      getGenericInfo() {
        let categories_url = `${api_url}/categories`  
        axios.get(categories_url)
          .then((res) => {
            this.categories = res.data;
          })
          .catch((error) => {
            console.log(error);
          })
        let states_url = `${api_url}/states`
        axios.get(states_url)
          .then((res) => {
            this.states = res.data;
          })
          .catch((error) => {
            console.log(error);
          })
        let colors_url = `${api_url}/colors`
        axios.get(colors_url)
          .then((res) => {
            this.colors = res.data;
          })
          .catch((error) => {
            console.log(error);
          })
        let fuels_url = `${api_url}/fuels`
        axios.get(fuels_url)
          .then((res) => {
            this.fuels = res.data;
          })
          .catch((error) => {
            console.log(error);
          })
          this.getSearches();
      },
      async onCategoryChange() {
        this.$refs.topProgress.start()
        let url = `${api_url}/categories/${this.selected.category.value}`
        await axios.get(url)
          .then((res) => {
            this.bodystyles = res.data.bodystyles;
            this.marks = res.data.marks;
            this.gears = res.data.gearboxes;
            this.driverTypes = res.data.driverTypes;
          })
          .catch((error) => {
            console.log(error);
          })
        this.$refs.topProgress.done()
      },
      onStateChange() {
        let url = `${api_url}/states/${this.selected.state.value}/cities`
        axios.get(url)
          .then((res) => {
              this.cities = res.data;
          })
          .catch((error) => {
            console.log(error);
          })
      },
      onMarkChange() {
        let url = `${api_url}/categories/${this.selected.category.value}/marks/${this.selected.mark.value}/models`
        axios.get(url)
          .then((res) => {
              this.models = res.data;
          })
          .catch((error) => {
            console.log(error);
          })
      },
      async calculate() {
        this.$refs.topProgress.start()
        this.limit = 10;
        this.classifieds = [];
        this.showMore = false;
        this.average = 0;
        this.total = 0;
        this.arithmeticMean = 0;
        let url = `${api_url}/average`
        let components = {}
        for (const [key, data] of Object.entries(this.selected)) {
            if (data) {
                components[key] = data.value
            } else {
                components[key] = null
            }
        }
        const ret = [];
        for (let d in components) {
            if (components[d] instanceof Array && components[d].length == 0) {
                continue;
            }
            if (components[d]) {
               ret.push(encodeURIComponent(d) + '=' + encodeURIComponent(components[d]));
            }
        }
        let querystring = ret.join('&');
        let average_url = `${url}?${querystring}`
        await axios.get(average_url)
          .then((res) => {
              this.average = JSON.parse(res.data);
              this.total = this.average.total;
              this.arithmeticMean = `$${this.average.arithmeticMean.toFixed(2)}`;
              let ids = this.average.classifieds
              let prices = this.average.prices
              let classifieds = []
              for (let i = 0; i < ids.length; i += 1) {
                  let id = ids[i];
                  let url = `https://auto.ria.com/auto__${id}.html`
                  classifieds.push({id: id, url: url, price: `$${prices[i].toFixed(2)}`})
              }
              this.classifieds = classifieds;
          })
          .catch((error) => {
            console.log(error);
          })
          this.calculated = true;
          this.classifiedsLimited = this.classifieds.slice(0, this.limit);
          await this.saveSearch()
          await this.getSearches();
          this.$refs.topProgress.done()
      },
      nextPage () {
        this.limit += 10;
        let newLimited = this.classifiedsLimited.concat(
          this.classifieds.slice(this.start, this.limit));
        this.classifiedsLimited = newLimited;
        if(this.showMore) this.getMoreInfo();
        this.start += 10;
      },
      prevPage() {
        if (this.limit <= 10) {
          return;
        }
        this.limit -= 10;
        this.classifiedsLimited = this.classifiedsLimited.slice(0, this.limit);
      },
      async getSearches() {
          this.$refs.topProgress.start()
          try {
            let searches_url = `${api_url}/searches`
            const { data } = await axios.get(searches_url)
            this.searches = data
            this.error = false
            this.$refs.topProgress.done()
          } catch (e) {
            this.searches = null
            this.error = e
            this.$refs.topProgress.fail()
          }
    },
      applySearch(searchId) {
          for (let i = 0; i < this.searches.length; i += 1) {
            if (this.searches[i].id == searchId) {
                let selectedSearch = this.searches[i];
                this.selected = selectedSearch;
                this.calculate();
            }
          }
      },
      async deleteSearch(searchId) {
          const url = `${api_url}/searches/${searchId}`
          this.$refs.topProgress.start()
          await axios.delete(url)
            .then(function(response){
                console.log(response.data);
                this.$refs.topProgress.done()
            })
            .catch(function(error) {
                console.log(error);
            })
          await this.getSearches()
      },
      saveSearch() {
          let save_url = `${api_url}/searches`;
          axios.post(save_url, this.selected)
            .then(function (response) {
                console.log(response.data);
            })
            .catch(function (error) {
                console.log(error);
            })
      },
      async getMoreInfo () {
          this.$refs.topProgress.start()
          for (let i = 0; i < this.classifiedsLimited.length; i += 1) {
             if (this.classifiedsLimited[i].loaded) {
                continue;
             }
             let id = this.classifiedsLimited[i].id;
             let url = `${api_url}/classifieds/${id}`
             await axios.get(url)
               .then(response => {
                 let data = JSON.parse(response.data);
                 this.classifiedsLimited[i] = {
                    id: id,
                    url: this.classifiedsLimited[i].url,
                    price: this.classifiedsLimited[i].price,
                    loaded: true,
                    model: `${data.markName} ${data.modelName}`,
                    city: `${data.locationCityName}`,
                    year: `${data.autoData.year}`,
                    race: `${data.autoData.race}`,
                 }
               console.log(this.classifiedsLimited[i])
               this.$forceUpdate();
               })
               .catch(error => {
                 console.log(error);
                 this.$refs.topProgress.fail();
               })
          }
          this.$refs.topProgress.done();
      },
  },
  mounted() {
    this.getGenericInfo()
  },
  created () {
    let year = new Date().getFullYear();
    for (let i = year - 90; i <= year; i += 1) {
       this.years[year - i] = {name: i, value: i};
    }
  },
};
</script>
