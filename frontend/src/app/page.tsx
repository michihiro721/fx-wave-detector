'use client'

import { useEffect, useState } from 'react'

interface ApiResponse {
  message: string
  status: string
  version: string
}

interface PriceData {
  pair: string
  price: number
  bid: number
  ask: number
  timestamp: string
}

export default function Home() {
  const [apiData, setApiData] = useState<ApiResponse | null>(null)
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'error'>('connecting')
  const [priceData, setPriceData] = useState<PriceData | null>(null)
  const [alertCount] = useState(0)

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  useEffect(() => {
    // API接続確認
    fetch(`${API_URL}/`)
      .then(response => response.json())
      .then((data: ApiResponse) => {
        setApiData(data)
        setConnectionStatus('connected')
        
        // モック価格データを設定
        setPriceData({
          pair: 'USD/JPY',
          price: 150.245,
          bid: 150.242,
          ask: 150.248,
          timestamp: new Date().toLocaleTimeString()
        })
      })
      .catch(error => {
        console.error('API接続エラー:', error)
        setConnectionStatus('error')
      })

    // 価格更新シミュレーション
    const priceInterval = setInterval(() => {
      if (connectionStatus === 'connected') {
        const basePrice = 150.245
        const variation = (Math.random() - 0.5) * 0.1
        const newPrice = basePrice + variation
        
        setPriceData({
          pair: 'USD/JPY',
          price: Number(newPrice.toFixed(3)),
          bid: Number((newPrice - 0.003).toFixed(3)),
          ask: Number((newPrice + 0.003).toFixed(3)),
          timestamp: new Date().toLocaleTimeString()
        })
      }
    }, 2000)

    return () => clearInterval(priceInterval)
  }, [API_URL, connectionStatus])

  const StatusIndicator = ({ status }: { status: 'connecting' | 'connected' | 'error' }) => {
    const config = {
      connecting: { color: 'bg-yellow-400', text: '接続中', pulse: true },
      connected: { color: 'bg-green-400', text: 'オンライン', pulse: false },
      error: { color: 'bg-red-400', text: 'オフライン', pulse: false }
    }
    
    const { color, text, pulse } = config[status]
    
    return (
      <div className="flex items-center space-x-2">
        <div className={`w-3 h-3 rounded-full ${color} ${pulse ? 'animate-pulse' : ''}`} />
        <span className="text-sm font-medium text-gray-600">{text}</span>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* ヘッダー */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">FX</span>
                </div>
                <h1 className="text-xl font-semibold text-gray-900">Wave Detector</h1>
              </div>
            </div>
            
            <div className="flex items-center space-x-6">
              <StatusIndicator status={connectionStatus} />
              <div className="flex items-center space-x-2 text-sm text-gray-500">
                <span>アラート:</span>
                <span className="font-semibold text-gray-900">{alertCount}</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* メインコンテンツ */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* 価格表示エリア */}
        <div className="mb-8">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">USD/JPY</h2>
              <div className="text-xs text-gray-500">
                最終更新: {priceData?.timestamp || '--:--:--'}
              </div>
            </div>
            
            {priceData ? (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* 現在価格 */}
                <div className="text-center">
                  <div className="text-sm text-gray-500 mb-1">現在価格</div>
                  <div className="text-3xl font-bold text-gray-900">
                    {priceData.price}
                  </div>
                </div>
                
                {/* Bid/Ask */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="text-center">
                    <div className="text-sm text-gray-500 mb-1">Bid</div>
                    <div className="text-xl font-semibold text-red-600">
                      {priceData.bid}
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="text-sm text-gray-500 mb-1">Ask</div>
                    <div className="text-xl font-semibold text-blue-600">
                      {priceData.ask}
                    </div>
                  </div>
                </div>

                {/* スプレッド */}
                <div className="text-center">
                  <div className="text-sm text-gray-500 mb-1">スプレッド</div>
                  <div className="text-xl font-semibold text-gray-900">
                    {priceData ? ((priceData.ask - priceData.bid) * 100).toFixed(1) : '0.0'}
                  </div>
                  <div className="text-xs text-gray-500">pips</div>
                </div>
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                価格データを取得中...
              </div>
            )}
          </div>
        </div>

        {/* ダッシュボードグリッド */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* 波形検出状況 */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">波形検出</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">第1波</span>
                <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                  検出済み
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">第2波</span>
                <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                  分析中
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">第3波</span>
                <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
                  待機中
                </span>
              </div>
            </div>
          </div>

          {/* アラート設定 */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">通知設定</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">LINE通知</span>
                <div className="w-8 h-4 bg-gray-200 rounded-full relative">
                  <div className="w-4 h-4 bg-gray-400 rounded-full absolute left-0 top-0"></div>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">音声アラート</span>
                <div className="w-8 h-4 bg-blue-200 rounded-full relative">
                  <div className="w-4 h-4 bg-blue-600 rounded-full absolute right-0 top-0"></div>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">メール通知</span>
                <div className="w-8 h-4 bg-gray-200 rounded-full relative">
                  <div className="w-4 h-4 bg-gray-400 rounded-full absolute left-0 top-0"></div>
                </div>
              </div>
            </div>
          </div>

          {/* システム状況 */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">システム状況</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">API接続</span>
                <div className={`w-2 h-2 rounded-full ${
                  connectionStatus === 'connected' ? 'bg-green-400' : 
                  connectionStatus === 'connecting' ? 'bg-yellow-400' : 'bg-red-400'
                }`} />
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">データ更新</span>
                <div className="w-2 h-2 rounded-full bg-green-400" />
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">アラート機能</span>
                <div className="w-2 h-2 rounded-full bg-yellow-400" />
              </div>
            </div>
          </div>
        </div>

        {/* アクションエリア */}
        <div className="mt-8 bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">クイックアクション</h3>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <button className="flex items-center justify-center px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
              <span className="mr-2">📊</span>
              <span>チャート表示</span>
            </button>
            
            <button className="flex items-center justify-center px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors">
              <span className="mr-2">🔔</span>
              <span>アラート設定</span>
            </button>
            
            <button className="flex items-center justify-center px-4 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors">
              <span className="mr-2">📱</span>
              <span>LINE連携</span>
            </button>
            
            <button 
              onClick={() => window.open(`${API_URL}/docs`, '_blank')}
              className="flex items-center justify-center px-4 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
            >
              <span className="mr-2">📚</span>
              <span>API仕様</span>
            </button>
          </div>
        </div>

        {/* フッター情報 */}
        <div className="mt-8 text-center text-sm text-gray-500">
          <p>FX Wave Detector v{apiData?.version || '1.0.0'} - 第3波検出アラートシステム</p>
          <p className="mt-1">データ提供: OANDA API | 本番環境</p>
        </div>
      </main>
    </div>
  )
}