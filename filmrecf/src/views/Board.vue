<template>
  <div style="width: 100%; height: 100%">
    <el-dialog title="Enter your rating" :visible.sync="rateDialogVisible" width="30%">
      <el-rate v-model="rateValue" :colors="colors"> </el-rate>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="sendRating">Done</el-button>
      </span>
    </el-dialog>

    <el-dialog title="Find Film" :visible.sync="findDialogVisible" width="23%">
      <div style="display: flex; justify-content: center">
        <div style="line-height: 40px; font-size: medium; margin-right: 5%;">
          File Name:
        </div>
        <!-- TODO autofill -->
        <div>
          <el-input placeholder="Input the name of film" v-model="filmName" width="50">
          </el-input>
        </div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="searchFilm">Search</el-button>
      </span>
    </el-dialog>

    <el-dialog title="Find Result" :visible.sync="recDialogVisible" width="80%">
      <div style="width: 100%; display: flex; margin-top: 10px; flex-wrap: wrap;">
        <el-card :body-style="{ padding: '0px' }" style="width: 270px; margin-left: 2%; margin-top: 10px;">
          <div style="font-size: large;">Result</div>
          <img :src="'http://127.0.0.1:8848/static/' + findMovie.id + '.jpg'" class="image"
            style="width: 100%; display: block" />
          <div style="padding: 14px">
            <span
              style="margin-top: 12px; width: 20px; max-width: 2em;overflow: hidden;white-space: nowrap;text-overflow: ellipsis;">
              {{findMovie.name}}
            </span>
            <div style="margin-top: 13px;line-height: 12px;">
              <el-tag v-for="t in findMovie.genres" size="mini" :key="t" style="margin-right: 4px;"> {{t}} </el-tag>
              <el-button type="text" class="button"
                style="float: right; padding: 0px; padding-top: -5px; font-size: medium;" @click="openRating(findMovie.id)">
                Rating</el-button>
            </div>

          </div>
        </el-card>
        <el-card v-for="(m, idx) in recMovies" :key="m.id" :body-style="{ padding: '0px' }"
          style="width: 270px; margin-left: 2%; margin-top: 10px;">
          <div style="font-size: large;">Recommended movie-{{idx + 1}}</div>
          <img :src="'http://127.0.0.1:8848/static/' + m.id + '.jpg'" class="image"
            style="width: 100%; display: block" />
          <div style="padding: 14px">
            <span
              style="margin-top: 12px; width: 20px; max-width: 2em;overflow: hidden;white-space: nowrap;text-overflow: ellipsis;">
              {{m.name}}
            </span>
            <div style="margin-top: 13px;line-height: 12px;">
              <el-tag v-for="t in m.genres" size="mini" :key="t" style="margin-right: 4px;"> {{t}} </el-tag>
              <el-button type="text" class="button"
                style="float: right; padding: 0px; padding-top: -5px; font-size: medium;" @click="openRating(m.id)">
                Rating</el-button>
            </div>

          </div>
        </el-card>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="sendRating">Done</el-button>
      </span>
    </el-dialog>

    <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
      <el-menu-item index="1">Movies</el-menu-item>
      <el-submenu index="2">
        <template slot="title">Category</template>
        <el-menu-item index="2-1">Action</el-menu-item>
        <el-menu-item index="2-2">Adventure</el-menu-item>
        <el-menu-item index="2-3">Animation</el-menu-item>
        <el-menu-item index="2-4">Biography</el-menu-item>
        <el-menu-item index="2-5">Comedy</el-menu-item>
        <el-menu-item index="2-6">Crime</el-menu-item>
        <el-menu-item index="2-7">Drama</el-menu-item>
        <el-menu-item index="2-8">Family</el-menu-item>
        <el-menu-item index="2-9">History</el-menu-item>
      </el-submenu>

      <div style="
          margin-left: 90%;
          text-align: center;
          line-height: 100%;
          margin-top: 20px;
          display: flex;
        ">
        <div style="margin-right: 20px; margin-top: -10px;">
          <el-button icon="el-icon-search" circle @click="openSearchDialog"></el-button>
        </div>
        {{getTimeState()}}
      </div>
    </el-menu>

    <div style="width: 100%; height: 92%; margin-top: -1%; margin-left: 5%;">
      <div style="width: 100%; display: flex; margin-top: 10px; flex-wrap: wrap;">
        <el-card v-for="m in movieList" :key="m.id" :body-style="{ padding: '0px' }"
          style="width: 270px; margin-left: 2%; margin-top: 10px;">
          <img :src="'http://127.0.0.1:8848/static/' + m.id + '.jpg'" class="image"
            style="width: 100%; display: block" />
          <div style="padding: 14px">
            <span
              style="margin-top: 12px; width: 20px; max-width: 2em;overflow: hidden;white-space: nowrap;text-overflow: ellipsis;">
              {{m.name}}
            </span>
            <div style="margin-top: 13px;line-height: 12px;">
              <el-tag v-for="t in m.genres" size="mini" :key="t" style="margin-right: 4px;"> {{t}} </el-tag>
              <el-button type="text" class="button"
                style="float: right; padding: 0px; padding-top: -5px; font-size: medium;" @click="openRating(m.id)">
                Rating</el-button>
            </div>

          </div>
        </el-card>
      </div>
    </div>

    <el-pagination background layout="prev, pager, next" :total="totalPages" :page-size=12 :pager-count=13
      :current-page.sync="currentPage" @current-change="changeCurrentPage">
    </el-pagination>
  </div>
</template>

<script>
import api from '../api';

export default {
  name: "Board",
  components: {},
  data: () => ({
    rateDialogVisible: false,
    findDialogVisible: false,
    recDialogVisible: false,
    rateValue: "",
    colors: [],
    activeIndex: "1",
    currentPage: 0,
    totalPages: 0,
    filmName: "",
    label: -1,
    movieList: [],
    movieId: 0,
    recMovies: [],
    findMovie: {},
  }),
  async mounted() {
    await this.changeCurrentPage();
  },
  methods: {
    getTimeState() {
      let timeNow = new Date();
      let hours = timeNow.getHours();
      if (hours >= 6 && hours <= 10) {
        return "Good Morning"
      } else if (hours > 10 && hours <= 1) {
        return "Good Afternoon"
      } else {
        return "Good Evening"
      }
    },
    handleSelect() {
      if (this.activeIndex == "1") {
        // request some films
      }
    },
    async searchFilm() {
      if (this.filmName == "") {
        this.$message.error("You must fill in the film name");
        return;
      }
      const resp = await api.movie.SEARCH({
        name: this.filmName,
      })
      if (resp.movies === undefined) {
        this.$message.error("The film does not exist");
        this.findDialogVisible = false;
        return;
      }

      this.findMovie = resp.movies;
      this.recMovies = resp.rec;
      this.findDialogVisible = false;
      this.recDialogVisible = true;
    },
    openSearchDialog() {
      this.filmName = ""
      this.findDialogVisible = true

    },
    async changeCurrentPage() {
      const resp = await api.movie.MOVIES({
        page: this.currentPage,
        label: this.label
      })
      this.movieList = resp.movies
      this.totalPages = resp.total
    },
    openRating(id) {
      this.rateDialogVisible = true;
      this.movieId = id;
    },
    sendRating() {
      this.rateDialogVisible = false;
      api.movie.RATING({
        id: this.movieId,
        value: this.rateValue
      })
    }
  },
};
</script>
<style lang="scss" scoped>
body {
  background-color: #080710;
  margin: 0px;
}
</>
