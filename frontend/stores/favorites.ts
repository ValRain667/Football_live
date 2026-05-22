import { defineStore } from 'pinia';

interface FavoritesState {
  teams: number[];
  matches: number[];
}

export const useFavoritesStore = defineStore('favorites', {
  state: (): FavoritesState => ({
    teams: [],
    matches: [],
  }),

  actions: {
    toggleTeam(id: number) {
      const idx = this.teams.indexOf(id);
      if (idx >= 0) this.teams.splice(idx, 1);
      else this.teams.push(id);
      this.save();
    },
    toggleMatch(id: number) {
      const idx = this.matches.indexOf(id);
      if (idx >= 0) this.matches.splice(idx, 1);
      else this.matches.push(id);
      this.save();
    },
    isTeamFavorite(id: number) {
      return this.teams.includes(id);
    },
    isMatchFavorite(id: number) {
      return this.matches.includes(id);
    },
    save() {
      if (process.client) {
        localStorage.setItem('fav_teams', JSON.stringify(this.teams));
        localStorage.setItem('fav_matches', JSON.stringify(this.matches));
      }
    },
    init() {
      if (process.client) {
        this.teams = JSON.parse(localStorage.getItem('fav_teams') || '[]');
        this.matches = JSON.parse(localStorage.getItem('fav_matches') || '[]');
      }
    },
  },
});
