"""
Claude API Deep Analysis Module
Performs qualitative analysis on top-ranked stocks
"""

import anthropic
import time
import re
from typing import List, Dict, Optional
import json


class ClaudeAnalyzer:
    """Deep analysis using Claude API"""
    
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        """
        Initialize Claude API client
        
        Args:
            api_key: Anthropic API key
            model: Claude model to use (default: claude-sonnet-4)
        """
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
    
    def _extract_json(self, text: str) -> Dict:
        """
        Extract JSON from Claude's response, handling markdown code blocks
        
        Args:
            text: Response text from Claude
            
        Returns:
            Parsed JSON dict
        """
        # Try to extract JSON from markdown code blocks
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
            print(f"      JSON parse error: {e}")
            print(f"      Response preview: {text[:200]}...")
            return None
        
    def analyze_stock_deep(self, stock_data: Dict, news_articles: List[Dict]) -> Dict:
        """
        Perform comprehensive deep analysis on a single stock
        
        Args:
            stock_data: Stock analysis data from the main system
            news_articles: List of recent news articles
            
        Returns:
            Dict with Claude's analysis
        """
        print(f"  🤖 Claude analyzing {stock_data['symbol']}...")
        
        # Prepare context for Claude
        context = self._prepare_stock_context(stock_data, news_articles)
        
        # Get multiple analyses
        analyses = {}
        
        # 1. News Sentiment Analysis
        analyses['sentiment'] = self._analyze_sentiment(context, news_articles)
        
        # 2. Catalyst Identification
        analyses['catalysts'] = self._identify_catalysts(context, news_articles)
        
        # 3. Risk Assessment
        analyses['risks'] = self._assess_risks(context, news_articles)
        
        # 4. Bull/Bear Case
        analyses['thesis'] = self._generate_thesis(context, stock_data)
        
        # 5. Trading Recommendation
        analyses['recommendation'] = self._generate_recommendation(context, stock_data, analyses)
        
        return analyses
    
    def _prepare_stock_context(self, stock_data: Dict, news_articles: List[Dict]) -> str:
        """Prepare stock context for Claude"""
        
        context = f"""
Stock: {stock_data['symbol']} - {stock_data['company_name']}
Sector: {stock_data['sector']}
Price: ${stock_data['price']:.2f}
Market Cap: ${stock_data.get('market_cap', 0):,.0f}

Technical Metrics:
- Composite Score: {stock_data['total_score']:.2f}/10
- Momentum Score: {stock_data['momentum_score']:.2f}/10
- Volume Score: {stock_data['volume_score']:.2f}/10
- Technical Score: {stock_data['technical_score']:.2f}/10
- Catalyst Score: {stock_data['catalyst_score']:.2f}/10

Price Performance:
- Day Change: {stock_data['metrics']['day_change_pct']:.2f}%
- Week Change: {stock_data['metrics']['week_change_pct']:.2f}%
- Month Change: {stock_data['metrics']['month_change_pct']:.2f}%

Technical Indicators:
- RSI (14): {stock_data['metrics']['rsi_14']:.1f}
- Volume Ratio: {stock_data['metrics']['volume_ratio']:.2f}x average

Recent News Headlines:
"""
        
        for i, article in enumerate(news_articles[:5], 1):
            context += f"\n{i}. {article.get('title', 'No title')}"
            if article.get('publishedDate'):
                context += f" ({article['publishedDate']})"
        
        return context
    
    def _analyze_sentiment(self, context: str, news_articles: List[Dict]) -> Dict:
        """Analyze news sentiment in depth"""
        
        if not news_articles:
            return {
                'score': 5,
                'label': 'Neutral',
                'summary': 'No recent news available for sentiment analysis.',
                'key_themes': []
            }
        
        prompt = f"""Analyze the sentiment of recent news for this stock.

{context}

Provide a detailed sentiment analysis:
1. Overall sentiment score (0-10, where 0=very negative, 5=neutral, 10=very positive)
2. Sentiment label (Very Negative, Negative, Neutral, Positive, Very Positive)
3. Brief summary (2-3 sentences) of the overall news tone
4. Key themes in the news (list 3-5 main topics being discussed)

Format your response as JSON:
{{
  "score": <0-10>,
  "label": "<sentiment label>",
  "summary": "<your summary>",
  "key_themes": ["theme1", "theme2", "theme3"]
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Extract JSON from response (handle markdown code blocks)
            text = response.content[0].text
            result = self._extract_json(text)
            return result
            
        except Exception as e:
            print(f"    ⚠ Sentiment analysis error: {e}")
            return {
                'score': 5,
                'label': 'Neutral',
                'summary': 'Error analyzing sentiment.',
                'key_themes': []
            }
    
    def _identify_catalysts(self, context: str, news_articles: List[Dict]) -> Dict:
        """Identify potential catalysts"""
        
        prompt = f"""Identify potential catalysts (positive or negative events that could drive price movement) for this stock.

{context}

Analyze and identify:
1. Upcoming catalysts (earnings, product launches, regulatory decisions, etc.)
2. Recent catalysts that already occurred
3. Potential catalysts on the horizon
4. Rate each catalyst's potential impact (High/Medium/Low)
5. Expected timeframe for each catalyst

Format as JSON:
{{
  "upcoming_catalysts": [
    {{"event": "<description>", "impact": "<High/Medium/Low>", "timeframe": "<when>", "type": "<positive/negative>"}}
  ],
  "recent_catalysts": [
    {{"event": "<description>", "impact": "<High/Medium/Low>", "timing": "<when it happened>"}}
  ],
  "catalyst_score": <0-10, how catalyst-rich is this stock?>,
  "summary": "<brief overview of catalyst situation>"
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result = self._extract_json(response.content[0].text)
            if result:
                return result
            else:
                raise ValueError("Failed to parse JSON response")
            
        except Exception as e:
            print(f"    ⚠ Catalyst analysis error: {e}")
            return {
                'upcoming_catalysts': [],
                'recent_catalysts': [],
                'catalyst_score': 5,
                'summary': 'Unable to identify catalysts.'
            }
    
    def _assess_risks(self, context: str, news_articles: List[Dict]) -> Dict:
        """Assess potential risks"""
        
        prompt = f"""Assess the risks associated with this stock for short-term trading (< 2 months).

{context}

Identify and analyze:
1. Key risks (regulatory, competitive, market, operational, etc.)
2. Risk level for each (High/Medium/Low)
3. Likelihood of each risk materializing (High/Medium/Low)
4. Overall risk score for short-term trading
5. Any red flags that would make this a "avoid" situation

Format as JSON:
{{
  "risks": [
    {{"risk": "<description>", "severity": "<High/Medium/Low>", "likelihood": "<High/Medium/Low>", "category": "<type>"}}
  ],
  "overall_risk_score": <0-10, where 0=very risky, 10=very safe>,
  "risk_label": "<Very High/High/Moderate/Low/Very Low>",
  "red_flags": ["<flag1>", "<flag2>"],
  "summary": "<brief risk assessment>"
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result = self._extract_json(response.content[0].text)
            if result:
                return result
            else:
                raise ValueError("Failed to parse JSON response")
            
        except Exception as e:
            print(f"    ⚠ Risk analysis error: {e}")
            return {
                'risks': [],
                'overall_risk_score': 5,
                'risk_label': 'Unknown',
                'red_flags': [],
                'summary': 'Unable to assess risks.'
            }
    
    def _generate_thesis(self, context: str, stock_data: Dict) -> Dict:
        """Generate bull and bear thesis"""
        
        prompt = f"""Create a concise bull case and bear case for this stock as a SHORT-TERM trade (< 2 months).

{context}

Provide:
1. Bull Case: 3-5 key reasons why this could move UP in the short term
2. Bear Case: 3-5 key reasons why this could move DOWN in the short term
3. Which case is stronger based on current conditions?
4. Expected risk/reward ratio
5. Ideal entry and exit strategy

Format as JSON:
{{
  "bull_case": [
    "reason 1",
    "reason 2",
    "reason 3"
  ],
  "bear_case": [
    "reason 1",
    "reason 2",
    "reason 3"
  ],
  "stronger_case": "<bull/bear/neutral>",
  "conviction_level": "<High/Medium/Low>",
  "risk_reward": "<ratio like 1:3>",
  "entry_strategy": "<suggestion>",
  "exit_strategy": "<suggestion>",
  "summary": "<2-3 sentence overall thesis>"
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result = self._extract_json(response.content[0].text)
            if result:
                return result
            else:
                raise ValueError("Failed to parse JSON response")
            
        except Exception as e:
            print(f"    ⚠ Thesis generation error: {e}")
            return {
                'bull_case': [],
                'bear_case': [],
                'stronger_case': 'neutral',
                'conviction_level': 'Low',
                'risk_reward': 'Unknown',
                'entry_strategy': 'Unable to generate',
                'exit_strategy': 'Unable to generate',
                'summary': 'Unable to generate thesis.'
            }
    
    def _generate_recommendation(self, context: str, stock_data: Dict, analyses: Dict) -> Dict:
        """Generate final trading recommendation"""
        
        sentiment = analyses.get('sentiment', {})
        catalysts = analyses.get('catalysts', {})
        risks = analyses.get('risks', {})
        thesis = analyses.get('thesis', {})
        
        prompt = f"""Based on the comprehensive analysis, provide a final trading recommendation for this stock.

{context}

Analysis Summary:
- Sentiment Score: {sentiment.get('score', 5)}/10 ({sentiment.get('label', 'Unknown')})
- Catalyst Score: {catalysts.get('catalyst_score', 5)}/10
- Risk Score: {risks.get('overall_risk_score', 5)}/10 ({risks.get('risk_label', 'Unknown')})
- Stronger Case: {thesis.get('stronger_case', 'unknown')}
- Conviction: {thesis.get('conviction_level', 'Unknown')}

Provide:
1. Clear recommendation: Strong Buy / Buy / Hold / Avoid
2. Confidence level: High / Medium / Low
3. Suggested position size: Small / Medium / Large
4. Key reasons (3-5 bullet points)
5. Watch points (what to monitor)
6. Exit conditions (when to sell)
7. Time horizon for this trade

Format as JSON:
{{
  "recommendation": "<Strong Buy/Buy/Hold/Avoid>",
  "confidence": "<High/Medium/Low>",
  "position_size": "<Small/Medium/Large>",
  "key_reasons": ["reason1", "reason2", "reason3"],
  "watch_points": ["point1", "point2"],
  "exit_conditions": ["condition1", "condition2"],
  "time_horizon": "<days/weeks>",
  "summary": "<2-3 sentence final recommendation>"
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result = self._extract_json(response.content[0].text)
            if result:
                return result
            else:
                raise ValueError("Failed to parse JSON response")
            
        except Exception as e:
            print(f"    ⚠ Recommendation generation error: {e}")
            return {
                'recommendation': 'Hold',
                'confidence': 'Low',
                'position_size': 'Small',
                'key_reasons': [],
                'watch_points': [],
                'exit_conditions': [],
                'time_horizon': 'Unknown',
                'summary': 'Unable to generate recommendation.'
            }
    
    def comparative_ranking(self, stocks_data: List[Dict]) -> Dict:
        """
        Re-rank stocks based on qualitative analysis
        
        Args:
            stocks_data: List of stock data with Claude analyses
            
        Returns:
            Re-ranked list with reasoning
        """
        print(f"\n🤖 Claude performing comparative analysis on {len(stocks_data)} stocks...")
        
        # Prepare summary of all stocks
        stocks_summary = []
        for i, stock in enumerate(stocks_data, 1):
            claude_analysis = stock.get('claude_analysis', {})
            
            summary = f"""
{i}. {stock['symbol']} - {stock['company_name']}
   - Quantitative Score: {stock['total_score']:.2f}/10
   - Sentiment: {claude_analysis.get('sentiment', {}).get('label', 'Unknown')}
   - Recommendation: {claude_analysis.get('recommendation', {}).get('recommendation', 'Unknown')}
   - Risk Level: {claude_analysis.get('risks', {}).get('risk_label', 'Unknown')}
   - Key Catalyst: {claude_analysis.get('catalysts', {}).get('summary', 'None')[:100]}
"""
            stocks_summary.append(summary)
        
        prompt = f"""You are an expert trader analyzing the top stocks for SHORT-TERM trading (< 2 months).

Here are the top candidates with their quantitative scores and qualitative analysis:

{''.join(stocks_summary)}

Task: Re-rank these stocks from best to worst for short-term trading, considering:
1. Technical setup (quantitative scores)
2. News sentiment and catalysts
3. Risk/reward profile
4. Near-term catalysts
5. Overall conviction

Provide your ranking with brief reasoning for each pick.

Format as JSON:
{{
  "top_5": [
    {{
      "rank": 1,
      "symbol": "<TICKER>",
      "reason": "<1-2 sentence explanation>",
      "key_edge": "<what makes this the #1 pick>"
    }}
  ],
  "avoid": [
    {{
      "symbol": "<TICKER>",
      "reason": "<why to avoid>"
    }}
  ],
  "market_outlook": "<brief view on current market conditions>",
  "top_pick_summary": "<2-3 sentences on the absolute best pick>"
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result = self._extract_json(response.content[0].text)
            if result:
                return result
            else:
                raise ValueError("Failed to parse JSON response")
            
        except Exception as e:
            print(f"  ⚠ Comparative analysis error: {e}")
            return {
                'top_5': [],
                'avoid': [],
                'market_outlook': 'Unable to generate',
                'top_pick_summary': 'Unable to generate'
            }
