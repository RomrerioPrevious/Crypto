import pandas as pd
from ..config import Config
from .trading_environment import TradingEnvironment
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from rl.agents import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import EpsGreedyQPolicy


def train_bot(symbol: str, leverage: int, timeframe_to_trade: str, csv_train: str,
              window_size: int, initial_balance: int, episodes=5) -> str:
    # Load historical data for training
    data = pd.read_csv(csv_train)
    df = data.rename({
        "open": 1, "high": 2, "low": 3, "close": 4
    })

    # Create trading environment
    env = TradingEnvironment(df, window_size, initial_balance, leverage)

    # Define DQN model
    model = Sequential()
    model.add(Dense(64, input_shape=(10, 8), activation="relu"))
    model.add(Dense(32, activation="relu"))
    model.add(Dense(env.action_space.n, activation="linear"))
    model.compile(optimizer=Adam(learning_rate=0.0001), loss="mse")

    # Set up DQN agent
    memory = SequentialMemory(limit=5000, window_length=1)
    policy = EpsGreedyQPolicy(eps=0.1)
    dqn = DQNAgent(model=model, nb_actions=env.action_space.n, memory=memory, nb_steps_warmup=500,
                   target_model_update=1e-2, policy=policy)
    dqn.compile(Adam(learning_rate=0.0001), metrics=["mae"])

    # Train the agent
    dqn.fit(env, nb_steps=50000, visualize=False, verbose=1)

    # Add this line after the training is complete
    path = f"{Config.find_global_path()}resources\\\\crypto_model.h5"
    model.save(path)
    return path
