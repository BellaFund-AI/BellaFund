/**
 * Web3 wallet connection hook
 * Handles multi-chain authentication
 */
import { useWeb3React } from '@web3-react/core'
import { InjectedConnector } from '@web3-react/injected-connector'

const SUPPORTED_CHAINS = {
  BNB: 56,
  Solana: 0x3 // Mainnet-beta: 0x1, using testnet for demo
}

export const injected = new InjectedConnector({
  supportedChainIds: Object.values(SUPPORTED_CHAINS)
})

export default function useWallet() {
  const { activate, deactivate, account, chainId } = useWeb3React()
  
  const connect = async (chainType) => {
    try {
      await activate(injected, undefined, true)
      if (chainId !== SUPPORTED_CHAINS[chainType]) {
        throw new Error('Please switch network in your wallet')
      }
    } catch (error) {
      console.error('Connection failed:', error)
    }
  }

  return {
    account,
    chainId,
    connect,
    disconnect: deactivate
  }
} 