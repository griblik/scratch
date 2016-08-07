import React from 'react/addons';
import Voting from '../../src/components/Voting';
import {expect} from 'chai';

const {renderIntoDocument, scryRenderedDOMComponentsWithTag} = React.addons.TestUtils;

describe('Voting', () => {
	it('renders a pair of buttons', () => {
		const component = renderIntoDocument(<Voting pair={['a','b']} />);
		const buttons = scryRenderedDOMComponentsWithTag(component, 'button');
		
		expect(buttons.length).to.equal(2);
		expect(buttons[0].textContent).to.equal('a');
		expect(buttons[1].textContent).to.equal('b');
	});
})