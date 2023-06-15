from hntpy import Account, Hotspot, Validator

# ===================================

## sample account functionality
account = Account(address="51-character-account-address")

# get validators and hotspots associated with an account
validators = account.validators()
hotspots = account.hotspots()

# get a generator of rewards, in a given time window, for an account (optionally can also return a list)
rewards_generator = account.rewards(min_time="2022-01-01", max_time="2022-06-01", gen=True)

for batch in rewards_generator:
    for reward in batch:
        # do some processing with the reward here...

# ===================================

## sample hotspot functionality

hotspot = Hotspot(address="51-character-hotspot-address")

# get roles (activity) for a hotspot, can optionally provide timeframe and response limit
roles = hotspot.roles(min_time="2022-01-01", limit=100)

# get the total reward sum for the hotspot, optionally in a given timeframe
rewards = hotspot.rewards(min_time="2022-01-01", max_time="2022-06-01")

# get hotspots that the given hotspot witnessed over the last 5 days
witnessed = hotspot.witnessed()

# ===================================

## sample validator functionality

validator = Validator(address="51-character-validator-address")

# get roles (activity) for a hotspot, can optionally provide timeframe and response limit
roles = validator.roles(limit=200)