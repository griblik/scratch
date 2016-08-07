import {Map, fromJS} from 'immutable';
import {expect} from 'chai';

import makeStore from '../src/store';

describe('store', () => {
	it('is a redux store configured with the correct reducer', () => {
		const store = makeStore();

		store.dispatch({
			type: 'SET_ENTRIES',
			entries: ['a','b','c']
		});

		expect(store.getState()).to.equal(fromJS({
			entries: ['a','b','c']
		}));
	});
});