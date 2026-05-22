import { footballApi } from '~/services/football';

type AsyncData<T> = {
  data: Ref<T | null>;
  pending: Ref<boolean>;
  error: Ref<any>;
  refresh: () => Promise<void>;
};

export function useMatches(params?: Ref<{ date?: string; league_id?: number; status?: string }>) {
  return useAsyncData(
    () => `matches-${JSON.stringify(params?.value || {})}`,
    () => footballApi.getMatches(params?.value),
    { watch: [() => params?.value] }
  ) as AsyncData<any>;
}

export function useLiveMatches() {
  const result = useAsyncData('live-matches', () => footballApi.getLiveMatches()) as AsyncData<any>;
  return result;
}

export function useMatch(id: Ref<number>) {
  return useAsyncData(
    () => `match-${id.value}`,
    () => footballApi.getMatch(id.value),
    { watch: [id] }
  ) as AsyncData<any>;
}

export function useTeams(search?: Ref<string>) {
  return useAsyncData(
    () => `teams-${search?.value || 'all'}`,
    () => footballApi.getTeams(search?.value),
    { watch: [() => search?.value] }
  ) as AsyncData<any>;
}

export function useTeam(id: Ref<number>) {
  return useAsyncData(
    () => `team-${id.value}`,
    () => footballApi.getTeam(id.value),
    { watch: [id] }
  ) as AsyncData<any>;
}

export function useLeagues() {
  return useAsyncData('leagues', () => footballApi.getLeagues()) as AsyncData<any>;
}

export function useLeague(id: Ref<number>) {
  return useAsyncData(
    () => `league-${id.value}`,
    () => footballApi.getLeague(id.value),
    { watch: [id] }
  ) as AsyncData<any>;
}

export function useStandings(leagueId: Ref<number>, season?: Ref<string>) {
  return useAsyncData(
    () => `standings-${leagueId.value}-${season?.value || '2024'}`,
    () => footballApi.getStandings(leagueId.value, season?.value),
    { watch: [leagueId, () => season?.value] }
  ) as AsyncData<any>;
}
