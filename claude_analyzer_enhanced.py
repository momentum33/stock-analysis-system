"""
Claude API Deep Analysis Module - ENHANCED WITH OPTIONS TRADE IDEAS
Optimized prompts + Options strategies for short-term trading
"""

import anthropic
import time
import re
from typing import List, Dict, Optional
import json


class ClaudeAnalyzer:
    """Deep analysis using Claude API with optimized prompts and options strategies"""
    
    def __init__(self, api_key: str, model: str = "claude-opus-4-20250514"):
        """Initialize Claude API client"""
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
    
    def _extract_json(self, text: str) -> Dict:
        """Extract JSON from Claude's response with improved error handling"""
        # Try to find JSON in code blocks first
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find raw JSON
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = text
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"      ⚠ JSON parse error: {e}")
            print(f"      Attempted to parse: {json_str[:200]}...")
            return None
    
    def analyze_stock_deep(self, stock_data: Dict, news_articles: List[Dict]) -> Dict:
        """Perform comprehensive deep analysis including options strategies"""
        print(f"  🤖 Claude analyzing {stock_data['symbol']}...")
        
        context = self._prepare_stock_context(stock_data, news_articles)
        
        analyses = {}
        
        # Core analyses
        analyses['sentiment'] = self._analyze_sentiment(context, news_articles)
        analyses['catalysts'] = self._identify_catalysts(context, news_articles)
        analyses['risks'] = self._assess_risks(context, news_articles)
        analyses['thesis'] = self._generate_thesis(context, stock_data)
        
        # NEW: Options trade ideas (if options data available)
        if stock_data.get('options_analysis'):
            print(f"  📊 Generating options strategies...")
            analyses['options_strategies'] = self._generate_options_strategies(
                context, stock_data, analyses
            )
        
        # Final recommendation
        analyses['recommendation'] = self._generate_recommendation(
            context, stock_data, analyses
        )
        
        return analyses
    
    def _prepare_stock_context(self, stock_data: Dict, news_articles: List[Dict]) -> str:
        """Prepare comprehensive stock context with enhanced formatting"""
        lines = []
        
        # Header
        lines.append(f"STOCK: {stock_data['symbol']} - {stock_data['company_name']}")
        lines.append(f"SECTOR: {stock_data['sector']} | PRICE: ${stock_data['price']:.2f} | CAP: ${stock_data.get('market_cap', 0):,.0f}")
        
        # Technical Scores
        lines.append(f"\nSCORES: Total {stock_data['total_score']:.2f}/10 | Momentum {stock_data['momentum_score']:.2f}/10 | Volume {stock_data['volume_score']:.2f}/10")
        
        # Performance
        metrics = stock_data['metrics']
        lines.append(f"PERFORMANCE: Day {metrics['day_change_pct']:.2f}% | Week {metrics['week_change_pct']:.2f}% | Month {metrics['month_change_pct']:.2f}%")
        lines.append(f"INDICATORS: RSI {metrics['rsi_14']:.1f} | Volume {metrics['volume_ratio']:.2f}x avg")
        
        # Fundamental data
        if stock_data.get('financial_ratios'):
            ratios = stock_data['financial_ratios']
            pe = ratios.get('priceEarningsRatio', 'N/A')
            roe = ratios.get('returnOnEquity', 'N/A')
            if isinstance(roe, (int, float)):
                roe = f"{roe*100:.1f}%"
            debt_eq = ratios.get('debtEquityRatio', 'N/A')
            margin = ratios.get('netProfitMargin', 'N/A')
            if isinstance(margin, (int, float)):
                margin = f"{margin*100:.1f}%"
            
            lines.append(f"\nFUNDAMENTALS: P/E {pe} | ROE {roe} | Debt/Eq {debt_eq} | Margin {margin}")
        
        # Short interest
        if stock_data.get('short_interest_data'):
            si = stock_data['short_interest_data']
            short_pct = si.get('shortPercentOfFloat', 'N/A')
            days_cover = si.get('daysToCover', 'N/A')
            lines.append(f"SHORT INTEREST: {short_pct}% float | {days_cover} days to cover")
        
        # Growth metrics
        if stock_data.get('growth_metrics'):
            growth = stock_data['growth_metrics']
            rev = growth.get('revenueGrowth', 'N/A')
            eps = growth.get('epsgrowth', 'N/A')
            if isinstance(rev, (int, float)):
                rev = f"{rev*100:.1f}%"
            if isinstance(eps, (int, float)):
                eps = f"{eps*100:.1f}%"
            lines.append(f"GROWTH: Revenue {rev} | EPS {eps}")
        
        # Options data (ENHANCED)
        if stock_data.get('options_analysis'):
            options = stock_data['options_analysis']
            put_call = options.get('put_call_ratio', 'N/A')
            iv = options.get('atm_implied_volatility', 'N/A')
            if iv != 'N/A' and isinstance(iv, (int, float)):
                iv_pct = f"{float(iv)*100:.1f}%"
            else:
                iv_pct = iv
            
            total_vol = options.get('total_call_volume', 0) + options.get('total_put_volume', 0)
            call_vol = options.get('total_call_volume', 0)
            put_vol = options.get('total_put_volume', 0)
            net_delta = options.get('net_delta', 'N/A')
            
            lines.append(f"\nOPTIONS DATA:")
            lines.append(f"  P/C Ratio: {put_call} | ATM IV: {iv_pct}")
            lines.append(f"  Volume: {total_vol:,} total ({call_vol:,} calls, {put_vol:,} puts)")
            lines.append(f"  Net Delta: {net_delta} | Contracts: {options.get('total_contracts', 0):,}")
            
            # Add expirations available
            if options.get('near_term_expirations'):
                exps = options['near_term_expirations'][:3]
                lines.append(f"  Near expirations: {', '.join(exps)}")
        
        # Recent news
        lines.append("\nRECENT NEWS:")
        for i, article in enumerate(news_articles[:5], 1):
            title = article.get('title', 'No title')
            date = article.get('publishedDate', '')
            lines.append(f"  {i}. {title} ({date})")
        
        return '\n'.join(lines)
    
    def _analyze_sentiment(self, context: str, news_articles: List[Dict]) -> Dict:
        """Analyze sentiment with optimized prompt structure"""
        
        if not news_articles:
            return {
                'score': 5,
                'label': 'Neutral',
                'summary': 'No recent news available.',
                'key_themes': [],
                'sentiment_momentum': 'stable'
            }
        
        prompt = f"""<task>Analyze news sentiment for SHORT-TERM trading (2-8 week horizon)</task>

<context>
{context}
</context>

<instructions>
1. Focus on NEAR-TERM price impact (next 2-8 weeks)
2. Weight recent news MORE heavily than older news
3. Look for sentiment SHIFTS and ACCELERATION patterns
4. Assess if sentiment is already priced in or has room to run
5. Consider market reaction vs news quality

Sentiment Scale:
- 9-10: Extremely positive (major breakout potential)
- 7-8: Very positive (strong upside momentum)
- 6: Positive (modest upside bias)
- 5: Neutral (no clear direction)
- 4: Negative (modest downside risk)
- 2-3: Very negative (strong selling pressure)
- 0-1: Extremely negative (avoid at all costs)
</instructions>

<output_format>
Return ONLY valid JSON (no additional text):
{{
  "score": <0-10>,
  "label": "Extremely Positive|Very Positive|Positive|Neutral|Negative|Very Negative|Extremely Negative",
  "summary": "<2-3 concise sentences on narrative, direction, and trading opportunity>",
  "key_themes": ["theme1", "theme2", "theme3"],
  "sentiment_momentum": "accelerating_positive|reversing_positive|stable|weakening|accelerating_negative",
  "priced_in_assessment": "<brief assessment if sentiment is reflected in price>"
}}
</output_format>"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1200,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )
            result = self._extract_json(response.content[0].text)
            if not result:
                return {'score': 5, 'label': 'Neutral', 'summary': 'Parse error.', 'key_themes': [], 'sentiment_momentum': 'stable'}
            return result
        except Exception as e:
            print(f"    ⚠ Sentiment error: {e}")
            return {'score': 5, 'label': 'Neutral', 'summary': f'Error: {str(e)}', 'key_themes': [], 'sentiment_momentum': 'stable'}
    
    def _identify_catalysts(self, context: str, news_articles: List[Dict]) -> Dict:
        """Identify catalysts with enhanced specificity"""
        
        prompt = f"""<task>Identify actionable catalysts for SHORT-TERM trading (2-8 weeks)</task>

<context>
{context}
</context>

<instructions>
PRIORITY: Binary events with specific dates within 8 weeks

For EACH catalyst provide:
- Event: SPECIFIC description with EXACT DATE if available
- Impact: High (>10% move) | Medium (3-10%) | Low (<3%)
- Timeframe: Exact date or "in X days/weeks"
- Type: positive | negative | uncertain
- Surprise_potential: high (>50% chance of beating expectations) | medium | low
- Probability: <percentage if estimable>

Examples of GOOD catalysts:
- "Q4 earnings on Oct 28 - analyst consensus $2.15 EPS, guidance raise expected"
- "FDA PDUFA decision on Nov 15 - 70% approval odds based on Phase 3 data"
- "Product launch Nov 1 - pre-orders 2x higher than previous model"

RED FLAGS to note:
- Recent negative catalysts that may still be impacting price
- Catalyst convergence (multiple events close together)

Catalyst Quality Score (0-10):
- 9-10: Multiple high-impact catalysts with clear dates
- 7-8: Strong single catalyst or several medium catalysts
- 5-6: Weak catalysts or uncertain timing
- 3-4: No clear catalysts, generic events only
- 0-2: Negative catalysts or red flags
</instructions>

<output_format>
Return ONLY valid JSON:
{{
  "upcoming_catalysts": [
    {{
      "event": "<specific event with date>",
      "impact": "High|Medium|Low",
      "timeframe": "<exact date or relative timing>",
      "type": "positive|negative|uncertain",
      "surprise_potential": "high|medium|low",
      "probability": "<% if estimable, else omit>"
    }}
  ],
  "recent_catalysts": [
    {{
      "event": "<what happened>",
      "impact": "<how it affected price>",
      "timing": "<when it occurred>",
      "priced_in": "fully|partially|not_yet"
    }}
  ],
  "catalyst_convergence": "<assessment if multiple catalysts align>",
  "catalyst_score": <0-10>,
  "summary": "<2-3 sentences on catalyst setup and timing>"
}}
</output_format>"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )
            result = self._extract_json(response.content[0].text)
            if not result:
                return {'upcoming_catalysts': [], 'catalyst_score': 5, 'summary': 'Parse error.'}
            return result
        except Exception as e:
            print(f"    ⚠ Catalyst error: {e}")
            return {'upcoming_catalysts': [], 'catalyst_score': 5, 'summary': f'Error: {str(e)}'}
    
    def _assess_risks(self, context: str, news_articles: List[Dict]) -> Dict:
        """Assess risks with enhanced red flag detection"""
        
        prompt = f"""<task>Assess downside risks for SHORT-TERM trade (2-8 weeks)</task>

<context>
{context}
</context>

<instructions>
Focus on IMMINENT risks (next 2 months). Prioritize specific, actionable risks.

For EACH risk provide:
- Risk: <specific concern>
- Severity: High (>15% drop potential) | Medium (5-15%) | Low (<5%)
- Likelihood: High (>50% chance) | Medium (20-50%) | Low (<20%)
- Timeframe: <when it could materialize>
- Category: regulatory|competitive|operational|management|technical|macro|other
- Mitigation: <any factors reducing this risk>

CRITICAL RED FLAGS (mention if present):
- Insider selling (especially by C-suite)
- Accounting irregularities or restatements
- SEC investigations or regulatory issues
- Key management departures
- Guidance cuts or analyst downgrades
- Technical breakdown below key support
- Debt covenant issues
- Failed clinical trials or product recalls

Risk Score (0-10):
- 9-10: Very low risk, strong setup
- 7-8: Low risk, manageable concerns
- 5-6: Moderate risk, proceed with caution
- 3-4: High risk, small position only
- 0-2: Very high risk, AVOID
</instructions>

<output_format>
Return ONLY valid JSON:
{{
  "risks": [
    {{
      "risk": "<specific risk>",
      "severity": "High|Medium|Low",
      "likelihood": "High|Medium|Low",
      "timeframe": "<when>",
      "category": "<category>",
      "mitigation": "<mitigating factors>"
    }}
  ],
  "red_flags": ["<flag1>", "<flag2>"],
  "overall_risk_score": <0-10>,
  "risk_label": "Very Low|Low|Moderate|High|Very High",
  "risk_vs_reward": "<assessment of risk/reward balance>",
  "position_size_guidance": "Large|Standard|Small|Avoid",
  "summary": "<2-3 sentences on risk profile>"
}}
</output_format>"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )
            result = self._extract_json(response.content[0].text)
            if not result:
                return {'risks': [], 'overall_risk_score': 5, 'risk_label': 'Unknown', 'summary': 'Parse error.'}
            return result
        except Exception as e:
            print(f"    ⚠ Risk error: {e}")
            return {'risks': [], 'overall_risk_score': 5, 'risk_label': 'Unknown', 'summary': f'Error: {str(e)}'}
    
    def _generate_options_strategies(self, context: str, stock_data: Dict, analyses: Dict) -> Dict:
        """NEW: Generate specific options trade ideas"""
        
        options = stock_data.get('options_analysis', {})
        sentiment = analyses.get('sentiment', {})
        catalysts = analyses.get('catalysts', {})
        risks = analyses.get('risks', {})
        
        # Build options-specific context
        options_context = f"""
OPTIONS METRICS:
- Put/Call Ratio: {options.get('put_call_ratio', 'N/A')}
- ATM Implied Volatility: {options.get('atm_implied_volatility', 'N/A')}
- Total Volume: {options.get('total_call_volume', 0) + options.get('total_put_volume', 0):,}
- Call Volume: {options.get('total_call_volume', 0):,}
- Put Volume: {options.get('total_put_volume', 0):,}
- Net Delta: {options.get('net_delta', 'N/A')}
- Available Expirations: {', '.join(options.get('near_term_expirations', [])[:5])}

ANALYSIS SCORES:
- Sentiment: {sentiment.get('score', 5)}/10 ({sentiment.get('label', 'Unknown')})
- Catalyst: {catalysts.get('catalyst_score', 5)}/10
- Risk: {risks.get('overall_risk_score', 5)}/10 ({risks.get('risk_label', 'Unknown')})
"""
        
        prompt = f"""<task>Generate SPECIFIC options trade ideas for short-term trading (2-8 weeks)</task>

<context>
{context}

{options_context}
</context>

<instructions>
Provide 2-3 SPECIFIC options strategies ranked by preference.

For EACH strategy provide:
1. Strategy Name: e.g., "Call Debit Spread", "Put Credit Spread", "Long Call", "Iron Condor"
2. Strikes: SPECIFIC strikes (e.g., "Buy 150 call, sell 155 call")
3. Expiration: SPECIFIC date from available expirations
4. Direction: bullish | bearish | neutral | volatility
5. Rationale: WHY this strategy fits (2-3 sentences, reference sentiment/catalysts/IV)
6. Max Risk: Dollar amount or percentage
7. Max Reward: Dollar amount or percentage  
8. Breakeven: Price level
9. Win Probability: <rough estimate>
10. Best Case: What needs to happen
11. Risk Factors: Key risks to this trade

Strategy Selection Guidelines:
- High IV (>40%): Consider credit spreads, iron condors, selling premium
- Low IV (<25%): Consider debit spreads, long calls/puts, buying premium
- High conviction + catalyst: Debit spreads or outright calls/puts
- Neutral/range-bound: Iron condors, strangles
- Bullish P/C ratio (<0.7): Calls or call spreads
- Bearish P/C ratio (>1.3): Puts or put spreads
- Near catalyst: Closer expiration, directional
- No clear catalyst: Further expiration, spreads

IMPORTANT: 
- Use expirations that align with catalyst timing
- If major catalyst in 3 weeks, use 4-5 week expiration
- Match strategy aggression to conviction level
- Consider liquidity (volume should be >100 for each leg)
</instructions>

<output_format>
Return ONLY valid JSON:
{{
  "strategies": [
    {{
      "rank": 1,
      "strategy_name": "<name>",
      "strikes": "<specific strikes>",
      "expiration": "<exact date from available>",
      "direction": "bullish|bearish|neutral|volatility",
      "rationale": "<why this works>",
      "max_risk": "<amount>",
      "max_reward": "<amount>",
      "breakeven": "<price>",
      "win_probability": "<estimate>",
      "best_case": "<what needs to happen>",
      "risk_factors": ["<factor1>", "<factor2>"]
    }}
  ],
  "iv_assessment": "overpriced|fair|underpriced",
  "liquidity_note": "<comment on options liquidity>",
  "summary": "<2-3 sentences on best approach>"
}}
</output_format>"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2500,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )
            result = self._extract_json(response.content[0].text)
            if not result:
                return {'strategies': [], 'summary': 'Parse error.'}
            return result
        except Exception as e:
            print(f"    ⚠ Options strategy error: {e}")
            return {'strategies': [], 'summary': f'Error: {str(e)}'}
    
    def _generate_thesis(self, context: str, stock_data: Dict) -> Dict:
        """Generate bull/bear thesis with enhanced structure"""
        
        prompt = f"""<task>Create actionable bull/bear thesis for 2-8 week trade</task>

<context>
{context}
</context>

<instructions>
Focus on SPECIFIC, TIMELY factors for short-term trading.

Bull Case Requirements:
- 3-5 SPECIFIC bullish factors
- At least 1-2 should be time-sensitive catalysts
- Include technical setup if favorable
- Mention momentum/sentiment if positive

Bear Case Requirements:
- 3-5 SPECIFIC bearish factors  
- Include any red flags or risks
- Mention technical resistance if relevant
- Note competitive/macro concerns

Additional Requirements:
- Stronger Case: Which side has more conviction (bull|bear|neutral)
- Conviction Level: High (>75% confidence) | Medium (50-75%) | Low (<50%)
- Risk/Reward Ratio: e.g., "1:3" (risking $1 to make $3)
- Entry Strategy: SPECIFIC - when to enter, what price, position size
- Exit Strategy: SPECIFIC - profit target, stop loss, time exit
- Time Horizon: Exact timeframe (e.g., "3-5 weeks", "hold through Oct 28 earnings")

Entry Timing Guidance:
- Immediate: Strong setup, catalyst coming soon
- Wait for pullback: Overbought but positive setup
- Wait for confirmation: Uncertain, need price action signal
- Avoid: Poor risk/reward or too many red flags
</instructions>

<output_format>
Return ONLY valid JSON:
{{
  "bull_case": ["<specific reason 1>", "<specific reason 2>", "..."],
  "bear_case": ["<specific reason 1>", "<specific reason 2>", "..."],
  "stronger_case": "bull|bear|neutral",
  "conviction_level": "High|Medium|Low",
  "risk_reward_ratio": "<ratio like 1:3>",
  "entry_strategy": "<specific entry guidance>",
  "exit_strategy": "<specific exit plan with targets and stops>",
  "time_horizon": "<specific timeframe>",
  "summary": "<2-3 sentences on overall thesis>"
}}
</output_format>"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2500,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )
            result = self._extract_json(response.content[0].text)
            if not result:
                return {'bull_case': [], 'bear_case': [], 'stronger_case': 'neutral', 'summary': 'Parse error.'}
            return result
        except Exception as e:
            print(f"    ⚠ Thesis error: {e}")
            return {'bull_case': [], 'bear_case': [], 'stronger_case': 'neutral', 'summary': f'Error: {str(e)}'}
    
    def _generate_recommendation(self, context: str, stock_data: Dict, analyses: Dict) -> Dict:
        """Generate final recommendation with options consideration"""
        
        sentiment = analyses.get('sentiment', {})
        catalysts = analyses.get('catalysts', {})
        risks = analyses.get('risks', {})
        thesis = analyses.get('thesis', {})
        has_options = 'options_strategies' in analyses
        
        options_note = ""
        if has_options:
            options_note = "\n\nOPTIONS STRATEGIES AVAILABLE - See separate options_strategies section for specific trade ideas."
        
        prompt = f"""<task>Make FINAL trading recommendation for 2-8 week trade</task>

<context>
{context}

ANALYSIS SUMMARY:
- Sentiment: {sentiment.get('score', 5)}/10 ({sentiment.get('label', 'Unknown')})
- Sentiment Momentum: {sentiment.get('sentiment_momentum', 'Unknown')}
- Catalyst Score: {catalysts.get('catalyst_score', 5)}/10
- Risk Score: {risks.get('overall_risk_score', 5)}/10 ({risks.get('risk_label', 'Unknown')})
- Stronger Case: {thesis.get('stronger_case', 'unknown')}
- Conviction: {thesis.get('conviction_level', 'Unknown')}
- Risk/Reward: {thesis.get('risk_reward_ratio', 'Unknown')}{options_note}
</context>

<instructions>
Recommendation Criteria:
- STRONG BUY: All factors align, high conviction, >1:2 R/R, catalyst in 2-4 weeks, low risk
- BUY: Mostly positive, medium conviction, >1:1.5 R/R, good setup
- HOLD: Mixed signals, wait for clarity or better entry point
- AVOID: Red flags, poor R/R, high risk, no edge

Confidence Guidelines:
- High: >75% confidence, clear edge, actionable setup
- Medium: 50-75% confidence, decent setup but some uncertainty
- Low: <50% confidence, marginal setup, many question marks

Position Size Guidelines:
- Large (5-10%): Highest conviction, best R/R, low risk, imminent catalyst
- Medium (3-5%): Good setup, standard conviction
- Small (1-2%): Speculative, lower conviction, higher risk
- None (0%): Avoid, too risky or no edge

Provide:
1. Clear recommendation with reasoning
2. Confidence level  
3. Position size guidance
4. 3-5 KEY reasons (most important factors)
5. 2-4 things to WATCH (price levels, news, dates)
6. Specific EXIT conditions (profit targets, stops, time exits)
7. Time horizon
8. One-line summary for quick reference
</instructions>

<output_format>
Return ONLY valid JSON:
{{
  "recommendation": "Strong Buy|Buy|Hold|Avoid",
  "confidence": "High|Medium|Low",
  "position_size": "Large|Medium|Small|None",
  "key_reasons": ["<reason 1>", "<reason 2>", "..."],
  "watch_points": ["<point 1>", "<point 2>", "..."],
  "exit_conditions": ["<condition 1>", "<condition 2>", "..."],
  "time_horizon": "<specific timeframe>",
  "trading_style": "stocks|options|both",
  "summary": "<1 sentence bottom line>"
}}
</output_format>"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )
            result = self._extract_json(response.content[0].text)
            if not result:
                return {'recommendation': 'Hold', 'confidence': 'Low', 'summary': 'Parse error.'}
            return result
        except Exception as e:
            print(f"    ⚠ Recommendation error: {e}")
            return {'recommendation': 'Hold', 'confidence': 'Low', 'summary': f'Error: {str(e)}'}
    
    def comparative_ranking(self, stocks_data: List[Dict]) -> Dict:
        """Re-rank stocks with enhanced criteria"""
        
        print(f"\n🤖 Claude performing comparative analysis on {len(stocks_data)} stocks...")
        
        stocks_summary = []
        for i, stock in enumerate(stocks_data, 1):
            ca = stock.get('claude_analysis', {})
            opts = stock.get('options_analysis', {})
            
            # Build summary line
            summary = f"{i}. {stock['symbol']} - Quant: {stock['total_score']:.2f}/10"
            summary += f" | Sent: {ca.get('sentiment', {}).get('score', 0):.1f}/10"
            summary += f" | Cat: {ca.get('catalysts', {}).get('catalyst_score', 0):.1f}/10"
            summary += f" | Risk: {ca.get('risks', {}).get('overall_risk_score', 0):.1f}/10"
            summary += f"\n   Rec: {ca.get('recommendation', {}).get('recommendation', 'Unknown')}"
            summary += f" ({ca.get('recommendation', {}).get('confidence', 'Unknown')} conf)"
            summary += f" | {ca.get('thesis', {}).get('stronger_case', 'Unknown')} case"
            
            # Add options note if available
            if opts:
                summary += f" | P/C: {opts.get('put_call_ratio', 'N/A')}"
                summary += f" | Options: Yes"
            
            stocks_summary.append(summary)
        
        prompt = f"""<task>Rank stocks BEST TO WORST for short-term trading (2-8 weeks)</task>

<stocks>
{''.join(stocks_summary)}
</stocks>

<instructions>
Re-rank from BEST to WORST using these criteria:

RANKING FACTORS (weighted):
1. Catalyst Timing (30%): Imminent catalyst (2-4 weeks) scores highest
2. Risk/Reward (25%): >1:2 ratio preferred
3. Technical Setup (20%): Strong momentum, good entry
4. Sentiment & Conviction (15%): Positive and accelerating
5. Options Setup (10%): Good liquidity, favorable P/C ratio

TOP 5 SELECTION CRITERIA:
- Clear catalyst within 4 weeks OR exceptional technical setup
- Risk/reward >1:2
- No major red flags
- Medium or High conviction
- Good liquidity (for stocks and options if using)

For TOP 5 provide:
- Rank (1-5)
- Symbol
- Reason (1-2 sentences - what's the edge?)
- Key Edge (specific advantage this stock has)
- Entry Timing (immediate|wait_for_pullback|wait_for_confirmation)
- Best Vehicle (stocks|options|both)

AVOID LIST:
- Stocks with red flags
- Poor risk/reward (<1:1)
- No clear catalyst or setup
- High risk scores
- Low liquidity in options (if options are key to thesis)

MARKET ASSESSMENT:
- Overall market conditions
- Sector trends affecting these stocks
- General risk appetite guidance
</instructions>

<output_format>
Return ONLY valid JSON:
{{
  "top_5": [
    {{
      "rank": 1,
      "symbol": "<ticker>",
      "reason": "<concise reason>",
      "key_edge": "<specific advantage>",
      "entry_timing": "immediate|wait_for_pullback|wait_for_confirmation",
      "best_vehicle": "stocks|options|both"
    }}
  ],
  "avoid": [
    {{
      "symbol": "<ticker>",
      "reason": "<why to avoid>"
    }}
  ],
  "market_outlook": "<2-3 sentences on overall market conditions>",
  "top_pick_summary": "<1-2 sentences on #1 pick>",
  "portfolio_approach": "<guidance on diversification and position sizing>"
}}
</output_format>"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )
            result = self._extract_json(response.content[0].text)
            if not result:
                return {'top_5': [], 'avoid': [], 'market_outlook': 'Parse error.'}
            return result
        except Exception as e:
            print(f"  ⚠ Comparative error: {e}")
            return {'top_5': [], 'avoid': [], 'market_outlook': f'Error: {str(e)}'}
