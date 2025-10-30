"""
Report Generator - Create CSV, HTML Dashboard, and PDF Report
"""
import csv
import os
from datetime import datetime
from typing import List, Dict
import config


class ReportGenerator:
    def __init__(self, output_dir: str = None):
        self.output_dir = output_dir or config.OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    def generate_all_reports(self, stocks: List[Dict], all_analyzed: int):
        """Generate all report formats"""
        csv_path = self.generate_csv(stocks)
        html_path = self.generate_html_dashboard(stocks, all_analyzed)
        pdf_path = self.generate_pdf_report(stocks, all_analyzed)
        
        return {
            'csv': csv_path,
            'html': html_path,
            'pdf': pdf_path
        }
    
    def generate_csv(self, stocks: List[Dict]) -> str:
        """Generate CSV output with all metrics"""
        filename = f"stock_analysis_{self.timestamp}.csv"
        filepath = os.path.join(self.output_dir, filename)
        
        if not stocks:
            print("No stocks to export to CSV")
            return None
        
        # Define CSV columns
        fieldnames = [
            'rank', 'symbol', 'company_name', 'total_score',
            'price', 'day_change_pct', 'volume', 'avg_volume', 'volume_ratio',
            'momentum_score', 'volume_score', 'technical_score', 
            'volatility_score', 'relative_strength_score', 'catalyst_score', 'liquidity_score',
            'rsi_14', 'week_change_pct', 'month_change_pct',
            'sma_10', 'sma_20', 'sma_50',
            'sector', 'market_cap', 'timestamp'
        ]
        
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for rank, stock in enumerate(stocks, 1):
                row = {
                    'rank': rank,
                    'symbol': stock['symbol'],
                    'company_name': stock['company_name'],
                    'total_score': f"{stock['total_score']:.2f}",
                    'price': f"{stock['price']:.2f}",
                    'day_change_pct': f"{stock['metrics']['day_change_pct']:.2f}",
                    'volume': stock['volume'],
                    'avg_volume': f"{stock['avg_volume']:.0f}",
                    'volume_ratio': f"{stock['metrics']['volume_ratio']:.2f}",
                    'momentum_score': f"{stock['momentum_score']:.2f}",
                    'volume_score': f"{stock['volume_score']:.2f}",
                    'technical_score': f"{stock['technical_score']:.2f}",
                    'volatility_score': f"{stock['volatility_score']:.2f}",
                    'relative_strength_score': f"{stock['relative_strength_score']:.2f}",
                    'catalyst_score': f"{stock['catalyst_score']:.2f}",
                    'liquidity_score': f"{stock['liquidity_score']:.2f}",
                    'rsi_14': f"{stock['metrics']['rsi_14']:.2f}",
                    'week_change_pct': f"{stock['metrics']['week_change_pct']:.2f}",
                    'month_change_pct': f"{stock['metrics']['month_change_pct']:.2f}",
                    'sma_10': f"{stock['metrics']['sma_10']:.2f}",
                    'sma_20': f"{stock['metrics']['sma_20']:.2f}",
                    'sma_50': f"{stock['metrics']['sma_50']:.2f}",
                    'sector': stock['sector'],
                    'market_cap': stock['market_cap'],
                    'timestamp': stock['timestamp'],
                }
                writer.writerow(row)
        
        print(f"CSV report generated: {filepath}")
        return filepath
    
    def generate_html_dashboard(self, stocks: List[Dict], all_analyzed: int) -> str:
        """Generate interactive HTML dashboard"""
        filename = f"dashboard_{self.timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stock Analysis Dashboard - {self.timestamp}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            color: #2d3748;
            margin-bottom: 10px;
        }}
        
        .header .stats {{
            display: flex;
            gap: 30px;
            margin-top: 20px;
        }}
        
        .stat {{
            background: #f7fafc;
            padding: 15px 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        
        .stat-label {{
            color: #718096;
            font-size: 0.85em;
            margin-bottom: 5px;
        }}
        
        .stat-value {{
            color: #2d3748;
            font-size: 1.5em;
            font-weight: bold;
        }}
        
        .stock-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(450px, 1fr));
            gap: 20px;
        }}
        
        .stock-card {{
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
            position: relative;
        }}
        
        .stock-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0,0,0,0.15);
        }}
        
        .rank-badge {{
            position: absolute;
            top: 15px;
            right: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.1em;
        }}
        
        .rank-badge.gold {{ background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); }}
        .rank-badge.silver {{ background: linear-gradient(135deg, #94a3b8 0%, #64748b 100%); }}
        .rank-badge.bronze {{ background: linear-gradient(135deg, #fb923c 0%, #f97316 100%); }}
        
        .stock-header {{
            margin-bottom: 15px;
        }}
        
        .symbol {{
            font-size: 1.8em;
            font-weight: bold;
            color: #2d3748;
            margin-bottom: 5px;
        }}
        
        .company-name {{
            color: #718096;
            font-size: 0.9em;
            margin-bottom: 5px;
        }}
        
        .sector {{
            display: inline-block;
            background: #e0e7ff;
            color: #5a67d8;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.75em;
            font-weight: 600;
            margin-top: 5px;
        }}
        
        .price-section {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 20px 0;
            padding: 15px;
            background: #f7fafc;
            border-radius: 8px;
        }}
        
        .price {{
            font-size: 2em;
            font-weight: bold;
            color: #2d3748;
        }}
        
        .change {{
            padding: 6px 12px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.95em;
        }}
        
        .change.positive {{
            background: #d1fae5;
            color: #059669;
        }}
        
        .change.negative {{
            background: #fee2e2;
            color: #dc2626;
        }}
        
        .score-section {{
            margin: 20px 0;
        }}
        
        .total-score {{
            text-align: center;
            margin-bottom: 15px;
        }}
        
        .total-score-label {{
            color: #718096;
            font-size: 0.85em;
            margin-bottom: 5px;
        }}
        
        .total-score-value {{
            font-size: 2.5em;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .score-bars {{
            display: grid;
            gap: 10px;
        }}
        
        .score-bar {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .score-label {{
            width: 120px;
            font-size: 0.85em;
            color: #4a5568;
            font-weight: 500;
        }}
        
        .score-track {{
            flex: 1;
            height: 8px;
            background: #e2e8f0;
            border-radius: 4px;
            overflow: hidden;
        }}
        
        .score-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 4px;
            transition: width 0.3s;
        }}
        
        .score-value {{
            width: 40px;
            text-align: right;
            font-weight: 600;
            color: #2d3748;
            font-size: 0.9em;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-top: 20px;
        }}
        
        .metric {{
            padding: 10px;
            background: #f7fafc;
            border-radius: 6px;
        }}
        
        .metric-label {{
            font-size: 0.75em;
            color: #718096;
            margin-bottom: 3px;
        }}
        
        .metric-value {{
            font-size: 1.1em;
            font-weight: 600;
            color: #2d3748;
        }}
        
        .news-section {{
            margin-top: 20px;
            padding-top: 20px;
            border-top: 2px solid #e2e8f0;
        }}
        
        .news-title {{
            font-size: 0.9em;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 10px;
        }}
        
        .news-item {{
            font-size: 0.8em;
            color: #4a5568;
            margin-bottom: 8px;
            padding-left: 12px;
            border-left: 3px solid #667eea;
        }}
        
        @media (max-width: 768px) {{
            .stock-grid {{
                grid-template-columns: 1fr;
            }}
            
            .header .stats {{
                flex-direction: column;
                gap: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📈 Top Stock Picks - Short Term Trading</h1>
            <p style="color: #718096; margin-top: 10px;">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <div class="stats">
                <div class="stat">
                    <div class="stat-label">Stocks Analyzed</div>
                    <div class="stat-value">{all_analyzed}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Top Picks</div>
                    <div class="stat-value">{len(stocks)}</div>
                </div>
                <div class="stat">
                    <div class="stat-label">Target Timeframe</div>
                    <div class="stat-value">&lt; 2 Months</div>
                </div>
            </div>
        </div>
        
        <div class="stock-grid">
"""
        
        for rank, stock in enumerate(stocks, 1):
            badge_class = 'gold' if rank == 1 else ('silver' if rank == 2 else ('bronze' if rank == 3 else ''))
            change = stock['metrics']['day_change_pct']
            change_class = 'positive' if change >= 0 else 'negative'
            change_symbol = '+' if change >= 0 else ''
            
            html_content += f"""
            <div class="stock-card">
                <div class="rank-badge {badge_class}">#{rank}</div>
                
                <div class="stock-header">
                    <div class="symbol">{stock['symbol']}</div>
                    <div class="company-name">{stock['company_name']}</div>
                    <span class="sector">{stock['sector']}</span>
                </div>
                
                <div class="price-section">
                    <div class="price">${stock['price']:.2f}</div>
                    <div class="change {change_class}">{change_symbol}{change:.2f}%</div>
                </div>
                
                <div class="score-section">
                    <div class="total-score">
                        <div class="total-score-label">Composite Score</div>
                        <div class="total-score-value">{stock['total_score']:.1f}</div>
                    </div>
                    
                    <div class="score-bars">
                        <div class="score-bar">
                            <div class="score-label">Momentum</div>
                            <div class="score-track">
                                <div class="score-fill" style="width: {stock['momentum_score']*10}%"></div>
                            </div>
                            <div class="score-value">{stock['momentum_score']:.1f}</div>
                        </div>
                        
                        <div class="score-bar">
                            <div class="score-label">Volume</div>
                            <div class="score-track">
                                <div class="score-fill" style="width: {stock['volume_score']*10}%"></div>
                            </div>
                            <div class="score-value">{stock['volume_score']:.1f}</div>
                        </div>
                        
                        <div class="score-bar">
                            <div class="score-label">Technical</div>
                            <div class="score-track">
                                <div class="score-fill" style="width: {stock['technical_score']*10}%"></div>
                            </div>
                            <div class="score-value">{stock['technical_score']:.1f}</div>
                        </div>
                        
                        <div class="score-bar">
                            <div class="score-label">Rel. Strength</div>
                            <div class="score-track">
                                <div class="score-fill" style="width: {stock['relative_strength_score']*10}%"></div>
                            </div>
                            <div class="score-value">{stock['relative_strength_score']:.1f}</div>
                        </div>
                        
                        <div class="score-bar">
                            <div class="score-label">Catalyst</div>
                            <div class="score-track">
                                <div class="score-fill" style="width: {stock['catalyst_score']*10}%"></div>
                            </div>
                            <div class="score-value">{stock['catalyst_score']:.1f}</div>
                        </div>
                    </div>
                </div>
                
                <div class="metrics-grid">
                    <div class="metric">
                        <div class="metric-label">RSI (14)</div>
                        <div class="metric-value">{stock['metrics']['rsi_14']:.1f}</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Week Change</div>
                        <div class="metric-value">{stock['metrics']['week_change_pct']:.1f}%</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Month Change</div>
                        <div class="metric-value">{stock['metrics']['month_change_pct']:.1f}%</div>
                    </div>
                    <div class="metric">
                        <div class="metric-label">Volume Ratio</div>
                        <div class="metric-value">{stock['metrics']['volume_ratio']:.2f}x</div>
                    </div>
                </div>
"""
            
            if stock.get('news') and len(stock['news']) > 0:
                html_content += """
                <div class="news-section">
                    <div class="news-title">📰 Recent News</div>
"""
                for news_item in stock['news'][:3]:
                    html_content += f"""
                    <div class="news-item">{news_item.get('title', 'No title')}</div>
"""
                html_content += """
                </div>
"""
            
            html_content += """
            </div>
"""
        
        html_content += """
        </div>
    </div>
</body>
</html>
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML dashboard generated: {filepath}")
        return filepath
    
    def generate_pdf_report(self, stocks: List[Dict], all_analyzed: int) -> str:
        """Generate PDF report (placeholder - requires reportlab or similar)"""
        filename = f"report_{self.timestamp}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("STOCK ANALYSIS REPORT - SHORT TERM TRADING (<2 MONTHS)\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Stocks Analyzed: {all_analyzed}\n")
            f.write(f"Top Picks: {len(stocks)}\n\n")
            
            f.write("=" * 80 + "\n")
            f.write("TOP PICKS\n")
            f.write("=" * 80 + "\n\n")
            
            for rank, stock in enumerate(stocks, 1):
                f.write(f"#{rank} - {stock['symbol']} ({stock['company_name']})\n")
                f.write("-" * 80 + "\n")
                f.write(f"Sector: {stock['sector']}\n")
                f.write(f"Price: ${stock['price']:.2f} ({stock['metrics']['day_change_pct']:+.2f}%)\n")
                f.write(f"Volume: {stock['volume']:,} (Avg: {stock['avg_volume']:,.0f}, Ratio: {stock['metrics']['volume_ratio']:.2f}x)\n\n")
                
                f.write(f"COMPOSITE SCORE: {stock['total_score']:.2f}/10\n\n")
                
                f.write("Score Breakdown:\n")
                f.write(f"  • Momentum:        {stock['momentum_score']:.2f}/10\n")
                f.write(f"  • Volume:          {stock['volume_score']:.2f}/10\n")
                f.write(f"  • Technical:       {stock['technical_score']:.2f}/10\n")
                f.write(f"  • Volatility:      {stock['volatility_score']:.2f}/10\n")
                f.write(f"  • Rel. Strength:   {stock['relative_strength_score']:.2f}/10\n")
                f.write(f"  • Catalyst:        {stock['catalyst_score']:.2f}/10\n")
                f.write(f"  • Liquidity:       {stock['liquidity_score']:.2f}/10\n\n")
                
                f.write("Key Metrics:\n")
                f.write(f"  • RSI (14):        {stock['metrics']['rsi_14']:.1f}\n")
                f.write(f"  • Week Change:     {stock['metrics']['week_change_pct']:+.2f}%\n")
                f.write(f"  • Month Change:    {stock['metrics']['month_change_pct']:+.2f}%\n")
                f.write(f"  • SMA 10/20/50:    ${stock['metrics']['sma_10']:.2f} / ${stock['metrics']['sma_20']:.2f} / ${stock['metrics']['sma_50']:.2f}\n\n")
                
                if stock.get('news') and len(stock['news']) > 0:
                    f.write("Recent News:\n")
                    for news_item in stock['news'][:3]:
                        f.write(f"  • {news_item.get('title', 'No title')}\n")
                    f.write("\n")
                
                f.write("\n")
        
        print(f"Text report generated: {filepath}")
        return filepath
