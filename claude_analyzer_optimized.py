"""
Claude API Deep Analysis Module - OPTIMIZED FOR OPUS 4
Enhanced prompts for maximum insight quality on short-term trades
"""

import anthropic
import time
import re
from typing import List, Dict, Optional
import json


class ClaudeAnalyzer:
    """Deep analysis using Claude API with optimized prompts"""
    
    def __init__(self, api_key: str, model: str = "claude-opus-4-20250514"):
        """Initialize Claude API client"""
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
    
    def _extract_json(self, text: str) -> Dict:
        """Extract JSON from Claude's response"""
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = text
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"      JSON parse error: {e}")
            return None
    
    def analyze_stock_deep(self, stock_data: Dict, news_articles: List[Dict]) -> Dict:
        """Perform comprehensive deep analysis"""
        print(f"  🤖 Claude analyzing {stock_data['symbol']}...")
        
        context = self._prepare_stock_context(stock_data, news_articles)
        
        analyses = {}
        analyses['sentiment'] = self._analyze_sentiment(context, news_articles)
        analyses['catalysts'] = self._identify_catalysts(context, news_articles)
        analyses['risks'] = self._assess_risks(context, news_articles)
        analyses['thesis'] = self._generate_thesis(context, stock_data)
        analyses['recommendation'] = self._generate_recommendation(context, stock_data, analyses)
        
        return analyses
    
    def _prepare_stock_context(self, stock_data: Dict, news_articles: List[Dict]) -> str:
        """Prepare stock context"""
        context = f"""Stock: {stock_data['symbol']} - {stock_data['company_name']}
Sector: {stock_data['sector']} | Price: ${stock_data['price']:.2f} | Market Cap: ${stock_data.get('market_cap', 0):,.0f}

Technical Scores: Composite {stock_data['total_score']:.2f}/10, Momentum {stock_data['momentum_score']:.2f}/10, Volume {stock_data['volume_score']:.2f}/10
Performance: Day {stock_data['metrics']['day_change_pct']:.2f}%, Week {stock_data['metrics']['week_change_pct']:.2f}%, Month {stock_data['metrics']['month_change_pct']:.2f}%
Indicators: RSI {stock_data['metrics']['rsi_14']:.1f}, Volume {stock_data['metrics']['volume_ratio']:.2f}x avg"""

        # Add fundamental data if available
        if stock_data.get('financial_ratios'):
            ratios = stock_data['financial_ratios']
            context += f"\n\nFundamentals: P/E {ratios.get('priceEarningsRatio', 'N/A')}, ROE {ratios.get('returnOnEquity', 'N/A')}, Debt/Equity {ratios.get('debtEquityRatio', 'N/A')}"
            context += f", Current Ratio {ratios.get('currentRatio', 'N/A')}, Net Margin {ratios.get('netProfitMargin', 'N/A')}"
        
        # Add short interest if available
        if stock_data.get('short_interest_data'):
            si = stock_data['short_interest_data']
            short_pct = si.get('shortPercentOfFloat', 'N/A')
            days_cover = si.get('daysaToCover', 'N/A')
            context += f"\nShort Interest: {short_pct}% of float, {days_cover} days to cover"
        
        # Add growth metrics if available
        if stock_data.get('growth_metrics'):
            growth = stock_data['growth_metrics']
            rev_growth = growth.get('revenueGrowth', 'N/A')
            eps_growth = growth.get('epsgrowth', 'N/A')
            context += f"\nGrowth: Revenue {rev_growth}, EPS {eps_growth}"
        
        # Add options data if available
        if stock_data.get('options_analysis'):
            options = stock_data['options_analysis']
            put_call = options.get('put_call_ratio', 'N/A')
            iv = options.get('atm_implied_volatility', 'N/A')
            if iv != 'N/A':
                iv = f"{float(iv)*100:.1f}%" if isinstance(iv, (int, float)) else iv
            total_vol = options.get('total_call_volume', 0) + options.get('total_put_volume', 0)
            context += f"\nOptions: Put/Call {put_call}, IV {iv}, Volume {total_vol:,}"
        
        context += "\n\nRecent News:"
        
        for i, article in enumerate(news_articles[:5], 1):
            context += f"\n{i}. {article.get('title', 'No title')}"
            if article.get('publishedDate'):
                context += f" ({article['publishedDate']})"
        
        return context
    
    def _analyze_sentiment(self, context: str, news_articles: List[Dict]) -> Dict:
        """Analyze sentiment optimized for short-term trading"""
        
        if not news_articles:
            return {'score': 5, 'label': 'Neutral', 'summary': 'No recent news.', 'key_themes': []}
        
        prompt = f"""You are an expert short-term trader (<2 months) analyzing news sentiment.

{context}

Focus on NEAR-TERM price impact (next 2-8 weeks), not fundamentals.
Weight recent news heavily. Look for sentiment SHIFTS and ACCELERATION.
Consider if sentiment is priced in or has momentum.

Provide:
1. Sentiment Score (0-10): 0-2 Very Negative, 3-4 Negative, 5 Neutral, 6-7 Positive, 8-10 Very Positive
2. Label: Very Negative | Negative | Neutral | Positive | Very Positive  
3. Summary: 2-3 sentences on narrative, direction, and short-term opportunity
4. Key Themes: 3-5 dominant topics
5. Sentiment Momentum: accelerating_positive | reversing_positive | stable | weakening | accelerating_negative

Return ONLY valid JSON:
{{
  "score": <0-10>,
  "label": "<label>",
  "summary": "<summary>",
  "key_themes": ["theme1", "theme2"],
  "sentiment_momentum": "<momentum>"
}}"""

        try:
            response = self.client.messages.create(model=self.model, max_tokens=1000, temperature=0.3,
                                                   messages=[{"role": "user", "content": prompt}])
            result = self._extract_json(response.content[0].text)
            return result if result else {'score': 5, 'label': 'Neutral', 'summary': 'Parse error.', 'key_themes': []}
        except Exception as e:
            print(f"    ⚠ Sentiment error: {e}")
            return {'score': 5, 'label': 'Neutral', 'summary': 'Error.', 'key_themes': []}
    
    def _identify_catalysts(self, context: str, news_articles: List[Dict]) -> Dict:
        """Identify catalysts with dates and impact"""
        
        prompt = f"""You are a catalyst-focused trader. Identify SPECIFIC, ACTIONABLE catalysts (<8 weeks).

{context}

Be SPECIFIC with DATES. Prioritize BINARY events. Consider SURPRISE potential and CONVERGENCE.

For each catalyst:
- Event: <specific with DATE>
- Impact: High (10%+ move) | Medium (3-10%) | Low (<3%)
- Timeframe: <date or "in X weeks">
- Type: positive | negative | uncertain
- Surprise_potential: high/medium/low
- Probability: <% if estimable>

Examples: "Q4 earnings Oct 28 - guidance raise expected", "FDA decision Nov 15 - 70% approval odds"

Also identify: Recent catalysts (last 2 weeks, priced in?), Catalyst convergence, Overall score 0-10

Return ONLY valid JSON:
{{
  "upcoming_catalysts": [{{"event": "", "impact": "", "timeframe": "", "type": "", "surprise_potential": "", "probability": ""}}],
  "recent_catalysts": [{{"event": "", "impact": "", "timing": "", "priced_in": ""}}],
  "catalyst_convergence": "",
  "catalyst_score": <0-10>,
  "summary": ""
}}"""

        try:
            response = self.client.messages.create(model=self.model, max_tokens=1800, temperature=0.3,
                                                   messages=[{"role": "user", "content": prompt}])
            result = self._extract_json(response.content[0].text)
            return result if result else {'upcoming_catalysts': [], 'catalyst_score': 5, 'summary': 'Parse error.'}
        except Exception as e:
            print(f"    ⚠ Catalyst error: {e}")
            return {'upcoming_catalysts': [], 'catalyst_score': 5, 'summary': 'Error.'}
    
    def _assess_risks(self, context: str, news_articles: List[Dict]) -> Dict:
        """Assess downside risks"""
        
        prompt = f"""You are a risk analyst for short-term trades (<2 months). Assess DOWNSIDE RISKS.

{context}

Focus on NEXT 2 MONTHS. Distinguish IMMINENT vs MEDIUM-TERM risks. Look for RED FLAGS.

For each risk:
- Risk: <specific>
- Severity: High (15%+ drop) | Medium (5-15%) | Low (<5%)
- Likelihood: High (>50%) | Medium (20-50%) | Low (<20%)
- Timeframe: <when>
- Category: regulatory/competitive/operational/management/technical/macro
- Mitigation: <being addressed?>

RED FLAGS: Insider selling, accounting issues, investigations, management exits, guidance cuts, technical breakdown

Risk Score (0-10): 0-2 Very High (avoid), 3-4 High (small position), 5-6 Moderate, 7-8 Low, 9-10 Very Low
Risk Label: Very High | High | Moderate | Low | Very Low

Return ONLY valid JSON:
{{
  "risks": [{{"risk": "", "severity": "", "likelihood": "", "timeframe": "", "category": "", "mitigation": ""}}],
  "red_flags": [""],
  "overall_risk_score": <0-10>,
  "risk_label": "",
  "risk_vs_reward": "",
  "summary": ""
}}"""

        try:
            response = self.client.messages.create(model=self.model, max_tokens=1800, temperature=0.3,
                                                   messages=[{"role": "user", "content": prompt}])
            result = self._extract_json(response.content[0].text)
            return result if result else {'risks': [], 'overall_risk_score': 5, 'risk_label': 'Unknown', 'summary': 'Parse error.'}
        except Exception as e:
            print(f"    ⚠ Risk error: {e}")
            return {'risks': [], 'overall_risk_score': 5, 'risk_label': 'Unknown', 'summary': 'Error.'}
    
    def _generate_thesis(self, context: str, stock_data: Dict) -> Dict:
        """Generate bull/bear thesis"""
        
        prompt = f"""Create ACTIONABLE bull/bear thesis for <2 month trade.

{context}

Focus on NEXT 2-8 WEEKS. Be SPECIFIC. Consider TIMING. Provide TACTICAL guidance.

Bull Case: 3-5 specific reasons (catalysts, technicals, momentum, sentiment)
Bear Case: 3-5 specific reasons (risks, resistance, fading momentum, negatives)
Stronger Case: bull | bear | neutral
Conviction: High (strong setup) | Medium (good but uncertain) | Low (marginal)
Risk/Reward: Ratio like "1:3"
Entry Strategy: When to enter, price levels, position size
Exit Strategy: Profit target, stop loss, time-based exit
Time Horizon: Specific timeframe

Return ONLY valid JSON:
{{
  "bull_case": [""],
  "bear_case": [""],
  "stronger_case": "",
  "conviction_level": "",
  "risk_reward": "",
  "entry_strategy": "",
  "exit_strategy": "",
  "time_horizon": "",
  "summary": ""
}}"""

        try:
            response = self.client.messages.create(model=self.model, max_tokens=2200, temperature=0.3,
                                                   messages=[{"role": "user", "content": prompt}])
            result = self._extract_json(response.content[0].text)
            return result if result else {'bull_case': [], 'bear_case': [], 'stronger_case': 'neutral', 'summary': 'Parse error.'}
        except Exception as e:
            print(f"    ⚠ Thesis error: {e}")
            return {'bull_case': [], 'bear_case': [], 'stronger_case': 'neutral', 'summary': 'Error.'}
    
    def _generate_recommendation(self, context: str, stock_data: Dict, analyses: Dict) -> Dict:
        """Generate final recommendation"""
        
        sentiment = analyses.get('sentiment', {})
        catalysts = analyses.get('catalysts', {})
        risks = analyses.get('risks', {})
        thesis = analyses.get('thesis', {})
        
        prompt = f"""Make FINAL TRADING RECOMMENDATION for <2 month trade.

{context}

Scores: Sentiment {sentiment.get('score', 5)}/10, Catalyst {catalysts.get('catalyst_score', 5)}/10, Risk {risks.get('overall_risk_score', 5)}/10
Thesis: {thesis.get('stronger_case', 'unknown')} case stronger, {thesis.get('conviction_level', 'Unknown')} conviction

Recommendation:
- Strong Buy: All align, high conviction, >1:2 risk/reward, catalyst in 2-4 weeks
- Buy: Mostly positive, medium conviction, >1:1.5 risk/reward
- Hold: Mixed signals, wait for clarity or better entry
- Avoid: Red flags, poor risk/reward, no edge

Confidence: High | Medium | Low
Position Size: Large (5-10%, highest conviction) | Medium (3-5%, standard) | Small (1-2%, speculative) | None (0%, avoid)
Key Reasons: 3-5 bullets why
Watch Points: 2-4 items to monitor
Exit Conditions: Profit target, stop loss, time/news-based exits
Time Horizon: How long to hold

Return ONLY valid JSON:
{{
  "recommendation": "",
  "confidence": "",
  "position_size": "",
  "key_reasons": [""],
  "watch_points": [""],
  "exit_conditions": [""],
  "time_horizon": "",
  "summary": ""
}}"""

        try:
            response = self.client.messages.create(model=self.model, max_tokens=1800, temperature=0.3,
                                                   messages=[{"role": "user", "content": prompt}])
            result = self._extract_json(response.content[0].text)
            return result if result else {'recommendation': 'Hold', 'confidence': 'Low', 'summary': 'Parse error.'}
        except Exception as e:
            print(f"    ⚠ Recommendation error: {e}")
            return {'recommendation': 'Hold', 'confidence': 'Low', 'summary': 'Error.'}
    
    def comparative_ranking(self, stocks_data: List[Dict]) -> Dict:
        """Re-rank stocks based on all analysis"""
        
        print(f"\n🤖 Claude performing comparative analysis on {len(stocks_data)} stocks...")
        
        stocks_summary = []
        for i, stock in enumerate(stocks_data, 1):
            ca = stock.get('claude_analysis', {})
            stocks_summary.append(f"""
{i}. {stock['symbol']} - Quant: {stock['total_score']:.2f}/10, Sentiment: {ca.get('sentiment', {}).get('score', 0):.1f}/10, Catalyst: {ca.get('catalysts', {}).get('catalyst_score', 0):.1f}/10, Risk: {ca.get('risks', {}).get('overall_risk_score', 0):.1f}/10
   Rec: {ca.get('recommendation', {}).get('recommendation', 'Unknown')} ({ca.get('recommendation', {}).get('confidence', 'Unknown')}), Case: {ca.get('thesis', {}).get('stronger_case', 'Unknown')}""")
        
        prompt = f"""You are a portfolio manager selecting BEST stocks for short-term trading (<2 months).

{''.join(stocks_summary)}

Re-rank BEST TO WORST. Consider ALL factors. Prioritize IMMINENT catalysts (2-4 weeks).

Selection Criteria for Top 5:
- Clear catalyst in 4 weeks OR exceptional technical
- Risk/reward >1:2
- No red flags
- Medium/High conviction

Ranking Factors: Catalyst Timing (30%), Risk/Reward (25%), Technical (20%), Sentiment (15%), Conviction (10%)

Provide Top 5 with: rank, symbol, reason (1-2 sentences), key_edge (specific advantage), entry_timing
Stocks to Avoid with red flags/poor setup: symbol, reason

Return ONLY valid JSON:
{{
  "top_5": [{{"rank": 1, "symbol": "", "reason": "", "key_edge": "", "entry_timing": ""}}],
  "avoid": [{{"symbol": "", "reason": ""}}],
  "market_outlook": "",
  "top_pick_summary": ""
}}"""

        try:
            response = self.client.messages.create(model=self.model, max_tokens=3500, temperature=0.3,
                                                   messages=[{"role": "user", "content": prompt}])
            result = self._extract_json(response.content[0].text)
            return result if result else {'top_5': [], 'avoid': [], 'market_outlook': 'Parse error.'}
        except Exception as e:
            print(f"  ⚠ Comparative error: {e}")
            return {'top_5': [], 'avoid': [], 'market_outlook': 'Error.'}
