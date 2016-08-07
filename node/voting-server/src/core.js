import {List, Map} from 'immutable';

export const INITIAL_STATE = Map();

function getWinners(vote) {
	if(!vote) return [];

	const [a,b] = vote.get('pair');
	const aVotes = vote.getIn(['tally', a], 0);
	const bVotes = vote.getIn(['tally', b], 0);

	if (aVotes > bVotes) return [a];
	else if (bVotes > aVotes) return [b];
	else return [a,b];
}

export function setEntries(state, movies) {
	return state.set('entries', List(movies));
}

export function next(state) {
	const entries = state.get('entries').concat(getWinners(state.get('vote')));

	if(entries.size === 1) {
		return state.remove('vote').remove('entries').set('winner', entries.first());
	} else { 
		return state.merge({
			vote: Map({pair: entries.take(2)}),
			entries: entries.skip(2)
		});
	}
}

export function vote(state, vote) {
	return state.updateIn(['tally', vote], 0, val => val + 1);
}