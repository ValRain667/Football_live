import api from './api';
import type { Match, Team, League, Standing } from '~/types';

export const footballApi = {
  async getMatches(params?: { date?: string; league_id?: number; status?: string }): Promise<Match[]> {
    const { data } = await api.get('/matches/', { params });
    return data;
  },

  async getLiveMatches(): Promise<Match[]> {
    const { data } = await api.get('/matches/live');
    return data;
  },

  async getMatch(id: number): Promise<Match> {
    const { data } = await api.get(`/matches/${id}`);
    return data;
  },

  async getTeams(search?: string): Promise<Team[]> {
    const { data } = await api.get('/teams/', { params: { search } });
    return data;
  },

  async getTeam(id: number): Promise<Team> {
    const { data } = await api.get(`/teams/${id}`);
    return data;
  },

  async getLeagues(): Promise<League[]> {
    const { data } = await api.get('/leagues/');
    return data;
  },

  async getLeague(id: number): Promise<League> {
    const { data } = await api.get(`/leagues/${id}`);
    return data;
  },

  async getStandings(leagueId: number, season?: string): Promise<Standing[]> {
    const { data } = await api.get(`/standings/${leagueId}`, { params: { season } });
    return data;
  },
};
