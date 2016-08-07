import {Map, fromJS, List} from 'immutable';
import {expect} from 'chai';

import reducer from '../src/reducer';

describe('reducer', () => {
	it('handles SET_ENTRIES', () => {
		const initialState = Map();
		const action = {type: 'SET_ENTRIES', entries: ['a', 'b', 'c']}
		const nextState = reducer(initialState, action);

		expect(nextState).to.equal(fromJS({entries: ['a','b','c']}));
	});
	
	it('handles NEXT', () => {
		const initialState = fromJS({
			entries: ['a','b']
		});
		const action = {type: 'NEXT'}
		const nextState = reducer(initialState, action);

		expect(nextState).to.equal(fromJS({vote:{pair: ['a', 'b']}, entries: []}));
	});

	it('handles VOTE', () => {
		const initialState = fromJS({vote: {pair: ['a', 'b']}, entries: []});
		const action = {type: 'VOTE', entry: 'a'};
		const nextState = reducer(initialState, action);

		expect(nextState).to.equal(fromJS({
			vote: {
				pair: ['a','b'],
				tally: {'a': 1}
			},
			entries: []
		}));
	});

	it('has an initial state', () => {
		const action = {type: 'SET_ENTRIES', entries: ['a']};
		const nextState = reducer(undefined, action);

		expect(nextState).to.equal(fromJS({
			entries: ['a']
		}));
	});

	it('can be used with reduce', () => {
		const actions = [
		    {type: 'SET_ENTRIES', entries: ['a', 'b']},
		    {type: 'NEXT'},
		    {type: 'VOTE', entry: 'a'},
		    {type: 'VOTE', entry: 'b'},
		    {type: 'VOTE', entry: 'a'},
		    {type: 'NEXT'}
	    ];

	    const finalState = actions.reduce(reducer, Map());

	    expect(finalState).to.equal(fromJS({winner: 'a'}));
	});
});