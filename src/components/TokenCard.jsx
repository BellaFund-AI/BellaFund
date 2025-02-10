/**
 * Interactive token rating display component
 * Shows AI score with visual indicators
 */
import { useWeb3 } from '@web3-react/core'

export default function TokenCard({ token }) {
  const { chainId } = useWeb3()
  
  const scoreColor = () => {
    if (token.score >= 75) return 'bg-green-100'
    if (token.score >= 50) return 'bg-yellow-100'
    return 'bg-red-100'
  }

  return (
    <div className={`p-4 rounded-lg ${scoreColor()}`}>
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-semibold">{token.symbol}</h3>
        <span className="text-2xl">{token.score}/100</span>
      </div>
      <div className="mt-2">
        <p className="text-sm text-gray-600">
          {chainId === 56 ? 'BNB Chain' : 'Solana'} Network
        </p>
        <div className="grid grid-cols-3 gap-2 mt-3">
          {token.factors.map((factor, index) => (
            <div key={index} className="p-2 bg-white rounded">
              <p className="text-xs capitalize">{factor.name}</p>
              <p className="text-sm font-medium">{factor.value}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
} 