#Registers parameters of every available type in order to test the rendering of the control panel, and runs a dummy model to test the Charts visualizer.

#===============
# PREAMBLE
#===============

from helipad import Helipad
heli = Helipad()
heli.name = 'Test'

#A handful of breeds and goods
breeds = [
	('hobbit', 'jam', '#D73229'),
	('dwarf', 'axe', '#2D8DBE'),
	('elf', 'lembas', '#CCBB22')
]
AgentGoods = {}
for b in breeds:
	heli.addBreed(b[0], b[2], prim='agent')
	heli.goods.add(b[1], b[2])

def gcallback(model, name, val):
	print(name, '=', val)

def icallback(model, name, item, val):
	print(name, '/', item, '=', val)

#===============
# ADD PARAMETERS
#===============

heli.params.add('gslider', 'Global slider', 'slider', dflt=1.5, opts={'low': 1, 'high': 5, 'step': 0.1}, callback=gcallback, desc="A global slider")
heli.params.add('gcheck', 'Global check', 'check', dflt=True, callback=gcallback, desc="A global checkbox")
heli.params.add('gmenu', 'Global menu', 'menu', dflt='two', opts={
	'one': 'Option one',
	'two': 'Option two',
	'three': 'Option three'
}, callback=gcallback, desc="A global menu")
heli.params.add('gcheckentry', 'Global Checkentry', 'checkentry', dflt='They\'re taking the hobbits to Isengard', callback=gcallback, desc="A global checkentry")
heli.params.add('glogslider', 'Global Logslider', 'slider', dflt=8, opts=[1,2,3,5,8,13,21,34], callback=gcallback, desc="A global logslider")

heli.params.add('islider', 'Item Slider', 'slider', per='breed', dflt={'hobbit': 0.1, 'dwarf': 0.3}, opts={'low':0, 'high': 1, 'step': 0.01}, callback=icallback, desc="A per-breed slider")
heli.params.add('icheck', 'Item Check', 'check', per='good', dflt={'jam': False, 'axe': True}, callback=icallback, desc="A per-good slider")
heli.params.add('imenu', 'Item Menu', 'menu', per='breed', dflt={'hobbit': 'three', 'dwarf': 'two'}, opts={
	'one': 'Option one',
	'two': 'Option two',
	'three': 'Option three'
}, callback=icallback, desc="A per-breed menu")
heli.params.add('icheckentry', 'Item Checkentry', 'checkentry', per='good', dflt={'jam': False, 'axe': 'wood'}, callback=icallback, desc="A per-good checkentry")
# heli.params.add('ilogslider', 'Item Logslider', 'slider', per='good', dflt={'axe': 5, 'lembas': 21}, opts=[1,2,3,5,8,13,21,34], callback=icallback, desc="A per-item logslider")

heli.params.add('gcheckgrid', 'Global Checkgrid', 'checkgrid',
	opts={'gondor':('Gondor', 'Currently calling for aid'), 'isengard':'Isengard', 'rohan':'Rohan', 'rivendell':'Rivendell', 'khazad':('Khazad-dûm', 'Nice diacritic')},
	dflt=['gondor', 'rohan', 'khazad'], callback=gcallback, desc="A global checkgrid"
)
heli.param('num_agent', 18)

#===============
# A DUMMY MODEL
# Testing the bar chart and network visualizers
#===============

import random
from helipad.visualize import Charts
viz = heli.useVisual(Charts)

@heli.hook
def agentInit(agent, model):
	for i in range(20): setattr(agent, 'prop'+str(i), 0)

@heli.hook
def agentStep(agent, model, stage):
	for i in range(20):
		v = getattr(agent, 'prop'+str(i))
		setattr(agent, 'prop'+str(i), v-1 if random.randint(0, 1) else v+1)

@heli.hook
def modelPostSetup(model):
	model.createNetwork(0.2)

def newedge(model):
	a1, a2 = random.choice(list(model.agents['agent'])), random.choice(list(model.agents['agent']))
	while a1.edgesWith(a2): a1, a2 = random.choice(list(model.agents['agent'])), random.choice(list(model.agents['agent']))
	a1.newEdge(a2, direction=random.choice([True, False]), weight=random.choice([0.5,1,2,3]))

#Cut one edge and create one edge
@heli.hook
def modelPostStep(model):
	random.choice(model.allEdges['edge']).cut()
	newedge(model)

net = viz.addPlot('net', 'Network Structure', type='network', layout='spring')
bar1 = viz.addPlot('prop', 'Bar Chart')
bar2 = viz.addPlot('prop2', 'Horizontal Bar Chart', horizontal=True)
net.config({
	'agentLabel': True,
 	'labelColor': '#FFFFFF',
# 	'labelFamily': 'serif',
	'agentMarker': 'H',
	'labelAlpha': 0.75,
	'labelWeight': 'bold',
 	'labelSize': 8
})

gcolors = ['F00', 'F03', 'F06', 'F09', 'F0C', 'C0F', '90F', '60F', '30F', '00F']
for i in range(20):
	heli.data.addReporter('prop'+str(i), heli.data.agentReporter('prop'+str(i), std=0.1))
	(bar1 if i<10 else bar2).addBar('prop'+str(i), str(i), '#'+gcolors[i%10])

#Replace an agent, but only if we click during the current model time
@heli.hook
def agentClick(agents, plot, t):
	if t != heli.t: return
	
	for agent in agents:
		new = agent.reproduce()
		enum = len(agent.edges[plot.kind]) if plot.kind in agent.edges else 0
		agent.die()
		for e in range(enum): newedge(heli)
		print('Killing agent',agent.id,'and creating agent',new.id)
	plot.update(None, t)
	plot.draw(t, forceUpdate=True)

#===============
# LAUNCH
#===============

heli.launchCpanel()