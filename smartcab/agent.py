import random
import math
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """ An agent that learns to drive in the Smartcab world.
        This is the object you will be modifying. """ 

    def __init__(self, env, learning=False, epsilon=1.0, alpha=0.5):
        super(LearningAgent, self).__init__(env)     # Set the agent in the evironment 
        self.planner = RoutePlanner(self.env, self)  # Create a route planner
        self.valid_actions = self.env.valid_actions  # The set of valid actions

        # Set parameters of the learning agent
        self.learning = learning # Whether the agent is expected to learn
        self.Q = dict()          # Create a Q-table which will be a dictionary of tuples
        self.epsilon = epsilon   # Random exploration factor
        self.alpha = alpha       # Learning factor

        ###########
        ## TO DO ##
        ###########
        # Set any additional class parameters as needed
        self.previous_state = ""
        self.previous_action = ""
        self.trial = 1.0

    def reset(self, destination=None, testing=False):
        """ The reset function is called at the beginning of each trial.
            'testing' is set to True if testing trials are being used
            once training trials have completed. """

        # Select the destination as the new location to route to
        self.planner.route_to(destination)
        
        ########### 
        ## TO DO ##
        ###########
        # Update epsilon using a decay function of your choice
        # Update additional class parameters as needed
        # If 'testing' is True, set epsilon and alpha to 0
        #MY CODE BEGINS
        if testing == True:
            self.epsilon = 0
            self.alpha = 0
        else:
            self.previous_action = ""
            self.previous_state = ""
            print "Trial: ", self.trial
            print "epsilon: ", self.epsilon
            import math
            #Cosine decay
            #self.epsilon = abs(math.cos(self.alpha * self.trial))
            #Linear decay (used for default leaner)
            self.epsilon = self.epsilon-0.001
            #self.epsilon = self.epsilon-0.001
            #Exponential decay (used for optimized learner)
            #self.epsilon = 1/self.trial**2
            #Alpha-driven decay
            #self.epsilon = self.alpha**self.trial
            self.trial = self.trial+1.0
            #print "Q Table: ", self.Q
        #MY CODE ENDS

        return None

    def build_state(self):
        """ The build_state function is called when the agent requests data from the 
            environment. The next waypoint, the intersection inputs, and the deadline 
            are all features available to the agent. """

        # Collect data about the environment
        waypoint = self.planner.next_waypoint() # The next waypoint 
        inputs = self.env.sense(self)           # Visual input - intersection light and traffic
        deadline = self.env.get_deadline(self)  # Remaining deadline

        ########### 
        ## TO DO ##
        ###########
        # Set 'state' as a tuple of relevant data for the agent
        #MY CODE BEGINS
        #print "inputs: ", inputs
        state = (waypoint, inputs['light'], inputs['oncoming'], inputs['left'])#, inputs['right'])#, deadline)
 #       state = (waypoint,inputs['light'])
        #MY CODE ENDS
        
        return state


    def get_maxQ(self, state):
        """ The get_max_Q function is called when the agent is asked to find the
            maximum Q-value of all actions based on the 'state' the smartcab is in. """

        ########### 
        ## TO DO ##
        ###########
        # Calculate the maximum Q-value of all actions for a given state

        maxQ = None
        #MY CODE BEGINS
        #Get highest q-value for best action
        maxQ = max(self.Q[state].values())
 
        #MY CODE ENDS
        return maxQ 


    def createQ(self, state):
        """ The createQ function is called when a state is generated by the agent. """

        ########### 
        ## TO DO ##
        ###########
        # When learning, check if the 'state' is not in the Q-table
        # If it is not, create a new dictionary for that state
        #   Then, for each action available, set the initial Q-value to 0.0
        #MY CODE BEGINS
        if self.learning == True:
            if not self.Q.has_key(state):
                action_q_val_pairs = {}
                for each in self.valid_actions:                
                    action_q_val_pairs[each] = 0.0
                self.Q[state] = action_q_val_pairs
        #print "Q: ", self.Q
        #MY CODE ENDS

        return


    def choose_action(self, state):
        """ The choose_action function is called when the agent is asked to choose
            which action to take, based on the 'state' the smartcab is in. """

        # Set the agent state and default action
        self.state = state
        self.next_waypoint = self.planner.next_waypoint()

        ########### 
        ## TO DO ##
        ###########
        # When not learning, choose a random action
        # When learning, choose a random action with 'epsilon' probability
        #   Otherwise, choose an action with the highest Q-value for the current state

        #MY CODE BEGINS
        use_qvalue = random.random()
        #print "use_qvalue: ", use_qvalue
        print "Trial: ", self.trial
        print "epsilon: ", self.epsilon

#        if not self.learning or use_qvalue > self.epsilon:
        if self.learning:
            if use_qvalue > self.epsilon:
                print "CHOOSING TO USE Q-TABLE ACTION"
                #Get action with highest q-value
                temp_action = ""
                max_q = self.get_maxQ(state)
                for each in self.Q[state].keys():
                    #print each, " action q value: ", self.Q[state][each]
                    temp_action = each
                    if self.Q[state][temp_action] == max_q:
                        action = temp_action
                        #print "found ", action, " with q: ", max_q
                        break
            else:
                print "CHOOSING RANDOM ACTION"
                random_index = random.randint(0,len(self.valid_actions)-1)            
                action = self.valid_actions[random_index]                
        else:
            print "CHOOSING RANDOM ACTION"
            random_index = random.randint(0,len(self.valid_actions)-1)            
            action = self.valid_actions[random_index]
        #print "Final action: ", action
        #MY CODE ENDS
        return action


    def learn(self, state, action, reward):
        """ The learn function is called after the agent completes an action and
            receives an award. This function does not consider future rewards 
            when conducting learning. """

        ########### 
        ## TO DO ##
        ###########
        # When learning, implement the value iteration update rule
        #   Use only the learning rate 'alpha' (do not use the discount factor 'gamma')
        #MY CODE BEGINS
        state_prime = state
        gamma = 0.0 #Per directive to "not use discount factor"

        if self.previous_state != "" and self.learning:
            print ">LEARNING<"

            #ORIGINAL ATTEMPT
            #oldQ = self.Q[self.previous_state][self.previous_action]
            #newQ = oldQ + (self.alpha*(reward + gamma*self.get_maxQ(state_prime) - oldQ))
            #self.Q[self.previous_state][self.previous_action] = newQ
            
            #WORKS FROM FORUMS:  self.Q[state][action] = (1.0-self.alpha) * self.Q[state][action] + (self.alpha * reward)
            
            #Iterative update equation
            oldQ = self.Q[state][action]
            newQ = oldQ + (self.alpha*(reward - oldQ))
            self.Q[state][action] = newQ
        self.previous_state = state
        self.previous_action = action
        #MY CODE ENDS

        return


    def update(self):
        """ The update function is called when a time step is completed in the 
            environment for a given trial. This function will build the agent
            state, choose an action, receive a reward, and learn if enabled. """

        state = self.build_state()          # Get current state
        self.createQ(state)                 # Create 'state' in Q-table
        action = self.choose_action(state)  # Choose an action
        reward = self.env.act(self, action) # Receive a reward
        self.learn(state, action, reward)   # Q-learn

        return
        

def run():
    """ Driving function for running the simulation. 
        Press ESC to close the simulation, or [SPACE] to pause the simulation. """

    ##############
    # Create the environment
    # Flags:
    #   verbose     - set to True to display additional output from the simulation
    #   num_dummies - discrete number of dummy agents in the environment, default is 100
    #   grid_size   - discrete number of intersections (columns, rows), default is (8, 6)
    env = Environment()
    
    ##############
    # Create the driving agent
    # Flags:
    #   learning   - set to True to force the driving agent to use Q-learning
    #    * epsilon - continuous value for the exploration factor, default is 1
    #    * alpha   - continuous value for the learning rate, default is 0.5
    agent = env.create_agent(LearningAgent, learning=True, alpha=0.5, epsilon=0.99) #added learning, alpha
    
    ##############
    # Follow the driving agent
    # Flags:
    #   enforce_deadline - set to True to enforce a deadline metric
    env.set_primary_agent(agent, enforce_deadline=True) #added enforce_deadline

    ##############
    # Create the simulation
    # Flags:
    #   update_delay - continuous time (in seconds) between actions, default is 2.0 seconds
    #   display      - set to False to disable the GUI if PyGame is enabled
    #   log_metrics  - set to True to log trial and simulation results to /logs
    #   optimized    - set to True to change the default log file name
    sim = Simulator(env, update_delay=0.0, log_metrics=True, display=False, optimized=True) #added update_delay & log_metric optimized
    
    ##############
    # Run the simulator
    # Flags:
    #   tolerance  - epsilon tolerance before beginning testing, default is 0.05 
    #   n_test     - discrete number of testing trials to perform, default is 0
    sim.run(n_test=20, tolerance=0.001) #added n_test & tolerance


if __name__ == '__main__':
    run()
