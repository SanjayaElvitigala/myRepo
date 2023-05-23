import random 
import numpy as np
import tensorflow as tf

from config import *

def create_model(learning_rate, state_shape, action_shape):

    initializer = tf.keras.initializers.HeUniform(seed=14542)
    model = tf.keras.Sequential()
    model.add( tf.keras.layers.Dense(600, input_shape=state_shape, activation='relu', kernel_initializer=initializer))
    model.add( tf.keras.layers.Dense(600, activation='relu', kernel_initializer=initializer))
    model.add( tf.keras.layers.Dense(action_shape, activation='linear', kernel_initializer=initializer))
    model.compile(loss= tf.keras.losses.Huber(), optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate), metrics=['accuracy'])
    return model

def train(pricing_algorithm,done):
    ALPHA = pricing_algorithm.ALPHA # Learning rate
    DISCOUNT =pricing_algorithm.DISCOUNT

    MIN_REPLAY_SIZE = pricing_algorithm.batch_end + 130
    if len(pricing_algorithm.replay_memory) < MIN_REPLAY_SIZE:
        return
    else:
        batch_size = 130
        mini_batch = pricing_algorithm.replay_memory[pricing_algorithm.batch_start : pricing_algorithm.batch_end]
        pricing_algorithm.batch_end +=130

        print(f"batch_start : {pricing_algorithm.batch_start} , batch_end : {pricing_algorithm.batch_end}")
        for type_of_room in room_type:
            current_states = np.array([transition[0][type_of_room] for transition in mini_batch])
            current_qs_list = pricing_algorithm.main_model.predict(current_states)
            new_current_states = np.array([transition[1][type_of_room] for transition in mini_batch])
            future_qs_list = pricing_algorithm.target_model.predict(new_current_states)

            X = []
            Y = []
            for index, (observation, new_observation, action, reward,  done) in enumerate(mini_batch):
                if not done:
                    max_future_q = reward[type_of_room] + DISCOUNT * np.max(future_qs_list[index])
                else:
                    max_future_q = reward[type_of_room]

                current_qs = current_qs_list[index]
                current_qs[action[type_of_room]] = (1 - ALPHA) * current_qs[action[type_of_room]] + ALPHA * max_future_q

            X.append(observation[type_of_room])
            Y.append(current_qs)
            pricing_algorithm.main_model.fit(np.array(X), np.array(Y), batch_size=batch_size, verbose=0)
 
  