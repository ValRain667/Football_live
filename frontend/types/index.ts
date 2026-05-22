export interface MatchTeam {
  id: number;
  name: string;
  logo?: string;
  score?: number | null;
}

export interface MatchEvent {
  time: string;
  type: string;
  player?: string;
  team: string;
}

export interface Match {
  id: number;
  home_team: MatchTeam;
  away_team: MatchTeam;
  league: string;
  league_logo?: string;
  status: string;
  minute?: number | null;
  date: string;
  events: MatchEvent[];
  possession?: Record<string, number> | null;
  statistics?: Record<string, any> | null;
}

export interface Team {
  id: number;
  name: string;
  logo?: string;
  country?: string;
  founded?: number;
  stadium?: string;
  coach?: string;
  squad?: any[];
  recent_matches?: any[];
  stats?: Record<string, any>;
}

export interface League {
  id: number;
  name: string;
  country?: string;
  logo?: string;
  season?: string;
  standings?: any[];
  top_scorers?: any[];
  top_assists?: any[];
}

export interface Standing {
  position: number;
  team: Team;
  played: number;
  won: number;
  draw: number;
  lost: number;
  goals_for: number;
  goals_against: number;
  goal_difference: number;
  points: number;
  form: string[];
}

export interface User {
  id: number;
  email: string;
  username: string;
  avatar?: string;
  created_at: string;
}
