from starknet_py.hash.address import compute_address
from starknet_py.net.account.account import Account
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.models import StarknetChainId
from starknet_py.net.signer.stark_curve_signer import KeyPair
import asyncio

async def deploy_account():
  # First, make sure to generate private key and salt

  key_pair = KeyPair.from_private_key(0x3e4a0938f64a1d08d83978cb5e1762fca85e5d7a9f6abd78f95cce5df56c8e9c)
  class_hash = 0x35ccefcf9d5656da623468e27e682271cd327af196785df99e7fee1436b6276
  salt = 0

  # Compute an address
  address = compute_address(
      salt=salt,
      class_hash=class_hash,  # class_hash of the Account declared on the Starknet
      constructor_calldata=[key_pair.public_key],
      deployer_address=0,
  )

  # Prefund the address (using the token bridge or by sending fee tokens to the computed address)
  # Make sure the tx has been accepted on L2 before proceeding

  # Define the client to be used to interact with Starknet
  client = FullNodeClient(node_url="ws://127.0.0.1:9944")
  chain = StarknetChainId.TESTNET

  # Use `Account.deploy_account` static method to deploy an account
  account_deployment_result = await Account.deploy_account(
      address=address,
      class_hash=class_hash,
      salt=salt,
      key_pair=key_pair,
      client=client,
      chain=chain,
      constructor_calldata=[key_pair.public_key],
      max_fee=int(1e15),
  )
  # Wait for deployment transaction to be accepted
  await account_deployment_result.wait_for_acceptance()

  # From now on, account can be used as usual
  account = account_deployment_result.account
  print('account: ', account)
  account

asyncio.run(deploy_account())
