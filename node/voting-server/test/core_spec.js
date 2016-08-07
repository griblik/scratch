import {List, Map} from 'immutable';
import {expect} from 'chai';

import {setEntries, next, vote} from '../src/core';

describe('application logic', () => {
	describe('setEntries', () => {
		it('adds the entries to the state', () => {
			const state = Map();
			const entries = List.of('a','b');
			const nextState = setEntries(state, entries);

			expect(nextState).to.equal(Map({
				entries: List.of('a','b')
			}));
		});
	});

	describe('next', () => {
		it('takes the next two entries into a vote', () => {
			const state = Map({'entries': List.of('a','b','c')});
			const nextState = next(state);

			expect(nextState).to.equal(Map({
				vote: Map({pair:List.of('a','b')}),
				entries:List.of('c')
			}));
		});

		it('puts the winner of the previous vote back in the list', () => {
			const state = Map({vote: Map({pair: List.of('a','b'), tally: Map({'a': 3, 'b': 2})}), entries: List.of('c', 'd', 'e')});
			const nextState = next(state);

			expect(nextState).to.equal(Map({vote: Map({pair: List.of('c','d')}), entries: List.of('e','a')}));
		});

		it('puts both entries from a tie back in the list', () => {
			const state = Map({vote: Map({pair: List.of('a','b'), tally: Map({'a': 3, 'b': 3})}), entries: List.of('c', 'd', 'e')});
			const nextState = next(state);

			expect(nextState).to.equal(Map({vote: Map({pair: List.of('c','d')}), entries: List.of('e','a','b')}));

		});

		it('marks a winner when just one entry left', () => {
			const state = Map({vote: Map({pair: List.of('a','b'), tally: Map({'a': 3, 'b': 2})}), entries: List.of()});
			const nextState = next(state);

			expect(nextState).to.equal(Map({winner: 'a'}));
		});
	});

	describe('vote', () => {
		it('creates a new tally for the voted entry', () => {
			const state = Map({pair: List.of('a','b')});
			const nextState = vote(state, 'a');

			expect(nextState).to.equal(Map({pair: List.of('a','b'), tally: Map({'a': 1})}));
		});

		it('adds to an existing tally for a voted entry', () => {
			const state = Map({pair: List.of('a','b'), tally: Map({'a': 3, 'b': 2})});
			const nextState = vote(state, 'a');

			expect(nextState).to.equal(Map({pair: List.of('a','b'), tally: Map({'a': 4, 'b': 2})}));
		});
	});
});