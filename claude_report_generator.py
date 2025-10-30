"""
Enhanced Report Generator with Claude Analysis
Creates reports including qualitative insights
"""

import csv
import os
from datetime import datetime
from typing import List, Dict
import config


class ClaudeReportGenerator:
    def __init__(self, output_dir: str = None):
        self.output_dir = output_dir or config.OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    def generate_all_reports(self, stocks: List[Dict], all_analyzed: int, comparative: Dict):
        """Generate all report formats with Claude insights"""
        csv_path = self.generate_csv(stocks)
        html_path = self.generate_html_dashboard(stocks, all_analyzed, comparative)
        pdf_path = self.generate_detailed_report(stocks, all_analyzed, comparative)
        
        return {
            'csv': csv_path,
            'html': html_path,
            'pdf': pdf_path
        }
    
    def generate_csv(self, stocks: List[Dict]) -> str:
        """Generate CSV with Claude analysis"""
        filename = f"stock_analysis_deep_{self.timestamp}.csv"
        filepath = os.path.join(self.output_dir, filename)
        
        if not stocks:
            return None
        
        fieldnames = [
            'rank', 'symbol', 'company_name', 'total_score', 'price',
            'sentiment_score', 'sentiment_label',
            'catalyst_score_claude', 'risk_score', 'risk_label',
            'recommendation', 'confidence', 'position_size',
            'stronger_case', 'conviction', 'time_horizon',
            'day_change_pct', 'week_change_pct', 'month_change_pct',
            'momentum_score', 'volume_score', 'technical_score',
            'sector', 'market_cap'
        ]
        
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for rank, stock in enumerate(stocks, 1):
                claude = stock.get('claude_analysis', {})
                sentiment = claude.get('sentiment', {})
                catalysts = claude.get('catalysts', {})
                risks = claude.get('risks', {})
                thesis = claude.get('thesis', {})
                rec = claude.get('recommendation', {})
                
                row = {
                    'rank': rank,
                    'symbol': stock['symbol'],
                    'company_name': stock['company_name'],
                    'total_score': f"{stock['total_score']:.2f}",
                    'price': f"{stock['price']:.2f}",
                    'sentiment_score': sentiment.get('score', 'N/A'),
                    'sentiment_label': sentiment.get('label', 'N/A'),
                    'catalyst_score_claude': catalysts.get('catalyst_score', 'N/A'),
                    'risk_score': risks.get('overall_risk_score', 'N/A'),
                    'risk_label': risks.get('risk_label', 'N/A'),
                    'recommendation': rec.get('recommendation', 'N/A'),
                    'confidence': rec.get('confidence', 'N/A'),
                    'position_size': rec.get('position_size', 'N/A'),
                    'stronger_case': thesis.get('stronger_case', 'N/A'),
                    'conviction': thesis.get('conviction_level', 'N/A'),
                    'time_horizon': rec.get('time_horizon', 'N/A'),
                    'day_change_pct': f"{stock['metrics']['day_change_pct']:.2f}",
                    'week_change_pct': f"{stock['metrics']['week_change_pct']:.2f}",
                    'month_change_pct': f"{stock['metrics']['month_change_pct']:.2f}",
                    'momentum_score': f"{stock['momentum_score']:.2f}",
                    'volume_score': f"{stock['volume_score']:.2f}",
                    'technical_score': f"{stock['technical_score']:.2f}",
                    'sector': stock['sector'],
                    'market_cap': stock['market_cap'],
                }
                writer.writerow(row)
        
        print(f"Enhanced CSV report generated: {filepath}")
        return filepath
    
    def generate_html_dashboard(self, stocks: List[Dict], all_analyzed: int, comparative: Dict) -> str:
        """Generate enhanced HTML dashboard with Claude insights"""
        filename = f"dashboard_deep_{self.timestamp}.html"
        filepath = os.path.join(self.output_dir, filename)
        
        # Handle None or malformed comparative data
        if not comparative or not isinstance(comparative, dict):
            comparative = {
                'market_outlook': 'Market analysis not available',
                'top_5': [],
                'avoid': []
            }
        
        # Enhanced HTML with Claude insights
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deep Stock Analysis - {self.timestamp}</title>
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
            max-width: 1600px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .ai-badge {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
            margin-left: 10px;
        }}
        
        .market-outlook {{
            background: #f7fafc;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
            border-left: 4px solid #667eea;
        }}
        
        .market-outlook h3 {{
            color: #2d3748;
            margin-bottom: 10px;
        }}
        
        .stock-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
            gap: 20px;
            max-width: 100%;
        }}
        
        .stock-card {{
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
            max-width: 650px;
        }}
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
        }}
        
        .recommendation {{
            display: inline-block;
            padding: 6px 14px;
            border-radius: 16px;
            font-weight: 600;
            font-size: 0.9em;
            margin: 10px 0;
        }}
        
        .rec-strong-buy {{ background: #d1fae5; color: #065f46; }}
        .rec-buy {{ background: #dbeafe; color: #1e40af; }}
        .rec-hold {{ background: #fef3c7; color: #92400e; }}
        .rec-avoid {{ background: #fee2e2; color: #991b1b; }}
        
        .sentiment {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 15px 0;
            padding: 12px;
            background: #f7fafc;
            border-radius: 8px;
        }}
        
        .sentiment-icon {{
            font-size: 1.5em;
        }}
        
        .claude-insight {{
            background: #f0f4ff;
            border-left: 3px solid #667eea;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }}
        
        .claude-insight h4 {{
            color: #667eea;
            margin-bottom: 8px;
            font-size: 0.95em;
        }}
        
        .bull-bear {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 15px 0;
        }}
        
        .bull-case {{
            background: #d1fae5;
            padding: 15px;
            border-radius: 8px;
        }}
        
        .bear-case {{
            background: #fee2e2;
            padding: 15px;
            border-radius: 8px;
        }}
        
        .bull-case h5, .bear-case h5 {{
            margin-bottom: 8px;
            font-size: 0.9em;
        }}
        
        .bull-case ul, .bear-case ul {{
            padding-left: 20px;
            font-size: 0.85em;
        }}
        
        .risk-indicator {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.75em;
            font-weight: 600;
            margin-left: 10px;
        }}
        
        .risk-very-low {{ background: #d1fae5; color: #065f46; }}
        .risk-low {{ background: #dbeafe; color: #1e40af; }}
        .risk-moderate {{ background: #fef3c7; color: #92400e; }}
        .risk-high {{ background: #fecaca; color: #991b1b; }}
        .risk-very-high {{ background: #fee2e2; color: #7f1d1d; }}
        
        /* Responsive breakpoints */
        @media (max-width: 900px) {{
            .stock-grid {{
                grid-template-columns: 1fr;
            }}
            .stock-card {{
                max-width: 100%;
            }}
            .bull-bear {{
                grid-template-columns: 1fr;
            }}
        }}
        
        @media (min-width: 901px) and (max-width: 1400px) {{
            .stock-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
        
        @media (min-width: 1401px) {{
            .stock-grid {{
                grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
            }}
        }}
        
        /* Ensure long text wraps properly */
        .stock-card p, .stock-card li {{
            word-wrap: break-word;
            overflow-wrap: break-word;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📈 Deep Stock Analysis<span class="ai-badge">🤖 AI-Enhanced</span></h1>
            <p style="color: #718096; margin-top: 10px;">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p style="color: #718096;">Powered by Claude AI for qualitative analysis</p>
            
            <div class="market-outlook">
                <h3>📊 Market Outlook</h3>
                <p>{comparative.get('market_outlook', 'Market analysis not available').replace('Parse error.', 'Comparative analysis unavailable - showing individual stock analyses below')}</p>
            </div>
"""
        
        if comparative.get('top_pick_summary'):
            html_content += f"""
            <div class="claude-insight" style="margin-top: 20px;">
                <h4>🎯 Top Pick Summary</h4>
                <p>{comparative['top_pick_summary']}</p>
            </div>
"""
        
        html_content += """
        </div>
        
        <div class="stock-grid">
"""
        
        # Validate we have stocks to display
        if not stocks or len(stocks) == 0:
            html_content += """
            <div class="stock-card" style="grid-column: 1/-1;">
                <h3 style="color: #991b1b;">⚠️ No Stocks Available</h3>
                <p>No stocks were analyzed with deep analysis. This could mean:</p>
                <ul>
                    <li>No stocks passed the initial filters</li>
                    <li>There was an error in the analysis process</li>
                    <li>The deep analysis was not enabled</li>
                </ul>
            </div>
"""
        else:
            # Generate stock cards
            for rank, stock in enumerate(stocks, 1):
                claude = stock.get('claude_analysis', {})
                
                # Skip stocks without Claude analysis
                if not claude or len(claude) == 0:
                    print(f"  ⚠ Warning: {stock.get('symbol', 'Unknown')} has no Claude analysis, skipping from dashboard")
                    continue
                
                sentiment = claude.get('sentiment', {})
                rec = claude.get('recommendation', {})
                risks = claude.get('risks', {})
                thesis = claude.get('thesis', {})
                catalysts = claude.get('catalysts', {})
            
                # Recommendation class
                rec_text = rec.get('recommendation', 'Hold')
                rec_class = 'rec-' + rec_text.lower().replace(' ', '-')
                
                # Risk class
                risk_label = risks.get('risk_label', 'Unknown').replace(' ', '-').lower()
                risk_class = f'risk-{risk_label}'
                
                # Sentiment emoji
                sentiment_score = sentiment.get('score', 5)
                if sentiment_score >= 7:
                    sentiment_emoji = '😊'
                elif sentiment_score >= 4:
                    sentiment_emoji = '😐'
                else:
                    sentiment_emoji = '😟'
                
                html_content += f"""
                <div class="stock-card">
                    <div style="position: relative;">
                        <h2 style="color: #2d3748; margin-bottom: 5px;">{stock['symbol']}</h2>
                        <p style="color: #718096; font-size: 0.9em;">{stock['company_name']}</p>
                        <p style="color: #667eea; font-size: 0.85em; margin-top: 5px;">Rank #{rank} | Score: {stock['total_score']:.2f}/10</p>
                        
                        <div class="recommendation {rec_class}" style="margin-top: 15px;">
                            {rec_text}
                            <span class="risk-indicator {risk_class}">{risks.get('risk_label', 'Unknown')} Risk</span>
                        </div>
                        
                        <div class="sentiment">
                            <span class="sentiment-icon">{sentiment_emoji}</span>
                            <div>
                                <strong>Sentiment:</strong> {sentiment.get('label', 'Unknown')} ({sentiment_score:.1f}/10)
                                <div style="font-size: 0.85em; color: #718096; margin-top: 5px;">
                                    {sentiment.get('summary', 'No sentiment data')}
                                </div>
                            </div>
                        </div>
                        
                        <div class="claude-insight">
                            <h4>🎯 Trading Recommendation</h4>
                            <p><strong>Confidence:</strong> {rec.get('confidence', 'Unknown')}</p>
                            <p><strong>Position Size:</strong> {rec.get('position_size', 'Unknown')}</p>
                            <p><strong>Time Horizon:</strong> {rec.get('time_horizon', 'Unknown')}</p>
                            <p style="margin-top: 8px;">{rec.get('summary', 'No recommendation available')}</p>
                        </div>
                        
                        <div class="bull-bear">
                            <div class="bull-case">
                                <h5>🐂 Bull Case {' (Stronger)' if thesis.get('stronger_case') == 'bull' else ''}</h5>
                                <ul>
    """
                
                for reason in thesis.get('bull_case', [])[:3]:
                    html_content += f"<li>{reason}</li>"
                
                html_content += f"""
                                </ul>
                            </div>
                            <div class="bear-case">
                                <h5>🐻 Bear Case {' (Stronger)' if thesis.get('stronger_case') == 'bear' else ''}</h5>
                                <ul>
    """
                
                for reason in thesis.get('bear_case', [])[:3]:
                    html_content += f"<li>{reason}</li>"
                
                html_content += f"""
                                </ul>
                            </div>
                        </div>
                        
                        <div class="claude-insight">
                            <h4>⚡ Key Catalysts</h4>
                            <p>{catalysts.get('summary', 'No catalyst information available')}</p>
                        </div>
                        
                        <div class="claude-insight">
                            <h4>⚠️ Key Risks</h4>
                            <p>{risks.get('summary', 'No risk information available')}</p>
    """
                
                if risks.get('red_flags'):
                    html_content += "<p style='margin-top: 8px;'><strong>Red Flags:</strong></p><ul>"
                    for flag in risks['red_flags'][:3]:
                        html_content += f"<li style='color: #991b1b;'>{flag}</li>"
                    html_content += "</ul>"
                
                html_content += """
                        </div>
                        
                        <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #e2e8f0; font-size: 0.85em; color: #718096;">
    """
                
                # Add options strategies if available
                options_strats = claude.get('options_strategies', {})
                if options_strats and options_strats.get('strategies'):
                    html_content += """
                        <div class="claude-insight" style="background: #fff7ed; border-left-color: #f59e0b;">
                            <h4 style="color: #f59e0b;">📈 Options Strategies</h4>
    """
                    for i, strat in enumerate(options_strats['strategies'][:3], 1):
                        html_content += f"""
                            <div style="margin: 10px 0; padding: 10px; background: white; border-radius: 4px;">
                                <strong>{i}. {strat.get('strategy_name', 'Unknown Strategy')}</strong>
                                <div style="margin-top: 5px; font-size: 0.9em;">
                                    <p><strong>Direction:</strong> {strat.get('direction', 'N/A').title()}</p>
                                    <p><strong>Strikes:</strong> {strat.get('strikes', 'N/A')}</p>
                                    <p><strong>Expiration:</strong> {strat.get('expiration', 'N/A')}</p>
                                    <p><strong>Max Risk:</strong> {strat.get('max_risk', 'N/A')}</p>
                                    <p><strong>Max Reward:</strong> {strat.get('max_reward', 'N/A')}</p>
                                    <p><strong>Breakeven:</strong> {strat.get('breakeven', 'N/A')}</p>
                                    <p><strong>Win Probability:</strong> {strat.get('win_probability', 'N/A')}</p>
                                    <p style="margin-top: 8px;"><strong>Rationale:</strong> {strat.get('rationale', 'N/A')}</p>
                                    <p style="margin-top: 8px;"><strong>Best Case:</strong> {strat.get('best_case', 'N/A')}</p>
    """
                        # Add risk factors if available
                        if strat.get('risk_factors'):
                            html_content += "<p style='margin-top: 8px;'><strong>Risk Factors:</strong></p><ul style='margin-left: 20px;'>"
                            for risk in strat.get('risk_factors', []):
                                html_content += f"<li style='font-size: 0.85em;'>{risk}</li>"
                            html_content += "</ul>"
                        
                        html_content += """
                            </div>
    """
                    html_content += """
                        </div>
    """
                
                if rec.get('key_reasons'):
                    html_content += "<strong>Key Reasons:</strong><ul>"
                    for reason in rec['key_reasons'][:3]:
                        html_content += f"<li>{reason}</li>"
                    html_content += "</ul>"
                
                html_content += """
                        </div>
                    </div>
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
        
        print(f"Enhanced HTML dashboard generated: {filepath}")
        return filepath
    
    def generate_detailed_report(self, stocks: List[Dict], all_analyzed: int, comparative: Dict) -> str:
        """Generate detailed text report with Claude insights"""
        filename = f"report_deep_{self.timestamp}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 100 + "\n")
            f.write("DEEP STOCK ANALYSIS REPORT - AI-ENHANCED\n")
            f.write("=" * 100 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Stocks Analyzed: {all_analyzed}\n")
            f.write(f"Deep Analysis: Top {len(stocks)} stocks\n")
            f.write(f"AI Model: Claude (Anthropic)\n\n")
            
            # Market Outlook
            f.write("=" * 100 + "\n")
            f.write("MARKET OUTLOOK\n")
            f.write("=" * 100 + "\n\n")
            f.write(f"{comparative.get('market_outlook', 'Not available')}\n\n")
            
            # Top Pick Summary
            if comparative.get('top_pick_summary'):
                f.write("=" * 100 + "\n")
                f.write("TOP PICK SUMMARY\n")
                f.write("=" * 100 + "\n\n")
                f.write(f"{comparative['top_pick_summary']}\n\n")
            
            # Individual Stock Analysis
            f.write("=" * 100 + "\n")
            f.write("DETAILED STOCK ANALYSIS\n")
            f.write("=" * 100 + "\n\n")
            
            for rank, stock in enumerate(stocks, 1):
                claude = stock.get('claude_analysis', {})
                
                f.write(f"{'='*100}\n")
                f.write(f"RANK #{rank}: {stock['symbol']} - {stock['company_name']}\n")
                f.write(f"{'='*100}\n\n")
                
                # Basic Info
                f.write(f"Price: ${stock['price']:.2f} | Sector: {stock['sector']}\n")
                f.write(f"Quantitative Score: {stock['total_score']:.2f}/10\n\n")
                
                # Recommendation
                rec = claude.get('recommendation', {})
                f.write(f"🎯 RECOMMENDATION: {rec.get('recommendation', 'N/A')}\n")
                f.write(f"   Confidence: {rec.get('confidence', 'N/A')}\n")
                f.write(f"   Position Size: {rec.get('position_size', 'N/A')}\n")
                f.write(f"   Time Horizon: {rec.get('time_horizon', 'N/A')}\n\n")
                f.write(f"   {rec.get('summary', 'No summary available')}\n\n")
                
                # Sentiment
                sentiment = claude.get('sentiment', {})
                f.write(f"📊 SENTIMENT ANALYSIS\n")
                f.write(f"   Score: {sentiment.get('score', 'N/A')}/10 ({sentiment.get('label', 'N/A')})\n")
                f.write(f"   {sentiment.get('summary', 'No sentiment data')}\n\n")
                
                if sentiment.get('key_themes'):
                    f.write(f"   Key Themes:\n")
                    for theme in sentiment['key_themes']:
                        f.write(f"     • {theme}\n")
                    f.write("\n")
                
                # Bull/Bear Case
                thesis = claude.get('thesis', {})
                f.write(f"🐂 BULL CASE ({thesis.get('conviction_level', 'Unknown')} conviction):\n")
                for reason in thesis.get('bull_case', []):
                    f.write(f"   • {reason}\n")
                f.write("\n")
                
                f.write(f"🐻 BEAR CASE:\n")
                for reason in thesis.get('bear_case', []):
                    f.write(f"   • {reason}\n")
                f.write("\n")
                
                f.write(f"   Stronger Case: {thesis.get('stronger_case', 'Unknown').upper()}\n")
                f.write(f"   Risk/Reward: {thesis.get('risk_reward', 'Unknown')}\n\n")
                
                # Catalysts
                catalysts = claude.get('catalysts', {})
                f.write(f"⚡ CATALYSTS (Score: {catalysts.get('catalyst_score', 'N/A')}/10):\n")
                f.write(f"   {catalysts.get('summary', 'No catalyst data')}\n\n")
                
                # Risks
                risks = claude.get('risks', {})
                f.write(f"⚠️  RISK ASSESSMENT ({risks.get('risk_label', 'Unknown')}):\n")
                f.write(f"   Risk Score: {risks.get('overall_risk_score', 'N/A')}/10\n")
                f.write(f"   {risks.get('summary', 'No risk data')}\n\n")
                
                if risks.get('red_flags'):
                    f.write(f"   🚩 Red Flags:\n")
                    for flag in risks['red_flags']:
                        f.write(f"      • {flag}\n")
                    f.write("\n")
                
                # Key Reasons
                if rec.get('key_reasons'):
                    f.write(f"💡 KEY REASONS:\n")
                    for reason in rec['key_reasons']:
                        f.write(f"   • {reason}\n")
                    f.write("\n")
                
                # Watch Points
                if rec.get('watch_points'):
                    f.write(f"👀 WATCH POINTS:\n")
                    for point in rec['watch_points']:
                        f.write(f"   • {point}\n")
                    f.write("\n")
                
                # Exit Conditions
                if rec.get('exit_conditions'):
                    f.write(f"🚪 EXIT CONDITIONS:\n")
                    for condition in rec['exit_conditions']:
                        f.write(f"   • {condition}\n")
                    f.write("\n")
                
                f.write("\n")
        
        print(f"Enhanced text report generated: {filepath}")
        return filepath
