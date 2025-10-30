"""
Data Collection System - Logs all analysis runs for future backtesting
Stores stock scores, recommendations, and market conditions in SQLite database
"""

import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional
import os


class DataCollector:
    """Collects and stores analysis data for backtesting"""
    
    def __init__(self, db_path: str = "data/analysis_history.db"):
        """Initialize data collector with database"""
        self.db_path = db_path
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Analysis runs table - one per script execution
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_runs (
                run_id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_date TEXT NOT NULL,
                run_timestamp TEXT NOT NULL,
                total_tickers INTEGER,
                passed_filters INTEGER,
                market_spy_price REAL,
                market_spy_change REAL,
                deep_analysis_enabled INTEGER,
                notes TEXT
            )
        """)
        
        # Stock analysis table - one per stock per run
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_analysis (
                analysis_id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER,
                ticker TEXT NOT NULL,
                company_name TEXT,
                sector TEXT,
                price REAL,
                market_cap REAL,
                
                -- Quantitative scores
                total_score REAL,
                momentum_score REAL,
                volume_score REAL,
                technical_score REAL,
                volatility_score REAL,
                relative_strength_score REAL,
                catalyst_score REAL,
                liquidity_score REAL,
                fundamental_score REAL,
                short_interest_score REAL,
                growth_score REAL,
                options_score REAL,
                
                -- Performance metrics
                day_change_pct REAL,
                week_change_pct REAL,
                month_change_pct REAL,
                volume_ratio REAL,
                rsi_14 REAL,
                
                -- Options data
                put_call_ratio REAL,
                options_volume INTEGER,
                atm_iv REAL,
                
                -- Short interest
                short_percent_float REAL,
                days_to_cover REAL,
                
                -- Fundamental data
                pe_ratio REAL,
                roe REAL,
                debt_equity REAL,
                revenue_growth REAL,
                eps_growth REAL,
                
                analysis_date TEXT NOT NULL,
                FOREIGN KEY (run_id) REFERENCES analysis_runs(run_id)
            )
        """)
        
        # Claude analysis table - qualitative insights
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS claude_analysis (
                claude_id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_id INTEGER,
                
                -- Sentiment
                sentiment_score REAL,
                sentiment_label TEXT,
                sentiment_momentum TEXT,
                
                -- Catalysts
                catalyst_score_claude REAL,
                upcoming_catalysts TEXT,  -- JSON
                
                -- Risks
                risk_score REAL,
                risk_label TEXT,
                red_flags TEXT,  -- JSON
                
                -- Thesis
                stronger_case TEXT,
                conviction_level TEXT,
                risk_reward_ratio TEXT,
                bull_case TEXT,  -- JSON
                bear_case TEXT,  -- JSON
                
                -- Recommendation
                recommendation TEXT,
                confidence TEXT,
                position_size TEXT,
                time_horizon TEXT,
                
                -- Options strategies
                has_options_strategies INTEGER,
                options_strategies TEXT,  -- JSON
                
                analysis_timestamp TEXT NOT NULL,
                FOREIGN KEY (analysis_id) REFERENCES stock_analysis(analysis_id)
            )
        """)
        
        # Trade log table - for tracking actual trades
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trade_log (
                trade_id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_id INTEGER,
                ticker TEXT NOT NULL,
                
                entry_date TEXT NOT NULL,
                entry_price REAL NOT NULL,
                position_size REAL,
                strategy_type TEXT,  -- 'stock' or 'options'
                
                -- For options
                option_type TEXT,  -- 'call' or 'put' or 'spread'
                strikes TEXT,
                expiration TEXT,
                contracts INTEGER,
                
                exit_date TEXT,
                exit_price REAL,
                pnl REAL,
                pnl_pct REAL,
                
                notes TEXT,
                FOREIGN KEY (analysis_id) REFERENCES stock_analysis(analysis_id)
            )
        """)
        
        # Create indexes for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_stock_ticker 
            ON stock_analysis(ticker, analysis_date)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_run_date 
            ON analysis_runs(run_date)
        """)
        
        conn.commit()
        conn.close()
        
        print(f"✅ Database initialized: {self.db_path}")
    
    def start_analysis_run(self, total_tickers: int, deep_analysis: bool = False, 
                          spy_price: float = None, spy_change: float = None,
                          notes: str = None) -> int:
        """Start a new analysis run and return run_id"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now()
        
        cursor.execute("""
            INSERT INTO analysis_runs 
            (run_date, run_timestamp, total_tickers, passed_filters, 
             market_spy_price, market_spy_change, deep_analysis_enabled, notes)
            VALUES (?, ?, ?, 0, ?, ?, ?, ?)
        """, (
            now.strftime('%Y-%m-%d'),
            now.isoformat(),
            total_tickers,
            spy_price,
            spy_change,
            1 if deep_analysis else 0,
            notes
        ))
        
        run_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return run_id
    
    def update_run_passed_filters(self, run_id: int, passed_count: int):
        """Update the count of stocks that passed filters"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE analysis_runs 
            SET passed_filters = ?
            WHERE run_id = ?
        """, (passed_count, run_id))
        
        conn.commit()
        conn.close()
    
    def log_stock_analysis(self, run_id: int, stock_data: Dict) -> int:
        """Log a single stock analysis and return analysis_id"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Extract data safely with defaults (handle None values)
        metrics = stock_data.get('metrics') or {}
        options = stock_data.get('options_analysis') or {}
        short = stock_data.get('short_interest_data') or {}
        ratios = stock_data.get('financial_ratios') or {}
        growth = stock_data.get('growth_metrics') or {}
        
        cursor.execute("""
            INSERT INTO stock_analysis (
                run_id, ticker, company_name, sector, price, market_cap,
                total_score, momentum_score, volume_score, technical_score,
                volatility_score, relative_strength_score, catalyst_score,
                liquidity_score, fundamental_score, short_interest_score,
                growth_score, options_score,
                day_change_pct, week_change_pct, month_change_pct,
                volume_ratio, rsi_14,
                put_call_ratio, options_volume, atm_iv,
                short_percent_float, days_to_cover,
                pe_ratio, roe, debt_equity, revenue_growth, eps_growth,
                analysis_date
            ) VALUES (
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?,
                ?, ?, ?,
                ?, ?, ?,
                ?, ?,
                ?, ?, ?,
                ?, ?,
                ?, ?, ?,
                ?, ?,
                ?, ?, ?, ?, ?,
                ?
            )
        """, (
            run_id,
            stock_data.get('symbol'),
            stock_data.get('company_name'),
            stock_data.get('sector'),
            stock_data.get('price'),
            stock_data.get('market_cap'),
            
            stock_data.get('total_score'),
            stock_data.get('momentum_score'),
            stock_data.get('volume_score'),
            stock_data.get('technical_score'),
            stock_data.get('volatility_score'),
            stock_data.get('relative_strength_score'),
            stock_data.get('catalyst_score'),
            stock_data.get('liquidity_score'),
            stock_data.get('fundamental_score'),
            stock_data.get('short_interest_score'),
            stock_data.get('growth_score'),
            stock_data.get('options_score'),
            
            metrics.get('day_change_pct'),
            metrics.get('week_change_pct'),
            metrics.get('month_change_pct'),
            metrics.get('volume_ratio'),
            metrics.get('rsi_14'),
            
            options.get('put_call_ratio'),
            options.get('total_call_volume', 0) + options.get('total_put_volume', 0),
            options.get('atm_implied_volatility'),
            
            short.get('shortPercentOfFloat'),
            short.get('daysToCover'),
            
            ratios.get('priceEarningsRatio'),
            ratios.get('returnOnEquity'),
            ratios.get('debtEquityRatio'),
            growth.get('revenueGrowth'),
            growth.get('epsgrowth'),
            
            datetime.now().strftime('%Y-%m-%d')
        ))
        
        analysis_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return analysis_id
    
    def log_claude_analysis(self, analysis_id: int, claude_data: Dict):
        """Log Claude's qualitative analysis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        sentiment = claude_data.get('sentiment') or {}
        catalysts = claude_data.get('catalysts') or {}
        risks = claude_data.get('risks') or {}
        thesis = claude_data.get('thesis') or {}
        recommendation = claude_data.get('recommendation') or {}
        options_strats = claude_data.get('options_strategies') or {}
        
        cursor.execute("""
            INSERT INTO claude_analysis (
                analysis_id,
                sentiment_score, sentiment_label, sentiment_momentum,
                catalyst_score_claude, upcoming_catalysts,
                risk_score, risk_label, red_flags,
                stronger_case, conviction_level, risk_reward_ratio,
                bull_case, bear_case,
                recommendation, confidence, position_size, time_horizon,
                has_options_strategies, options_strategies,
                analysis_timestamp
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
        """, (
            analysis_id,
            
            sentiment.get('score'),
            sentiment.get('label'),
            sentiment.get('sentiment_momentum'),
            
            catalysts.get('catalyst_score'),
            json.dumps(catalysts.get('upcoming_catalysts', [])),
            
            risks.get('overall_risk_score'),
            risks.get('risk_label'),
            json.dumps(risks.get('red_flags', [])),
            
            thesis.get('stronger_case'),
            thesis.get('conviction_level'),
            thesis.get('risk_reward_ratio'),
            json.dumps(thesis.get('bull_case', [])),
            json.dumps(thesis.get('bear_case', [])),
            
            recommendation.get('recommendation'),
            recommendation.get('confidence'),
            recommendation.get('position_size'),
            recommendation.get('time_horizon'),
            
            1 if options_strats.get('strategies') else 0,
            json.dumps(options_strats.get('strategies', [])),
            
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def log_trade(self, ticker: str, entry_date: str, entry_price: float,
                  position_size: float = None, strategy_type: str = 'stock',
                  option_type: str = None, strikes: str = None, 
                  expiration: str = None, contracts: int = None,
                  notes: str = None) -> int:
        """Log a trade entry"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Try to find most recent analysis_id for this ticker
        cursor.execute("""
            SELECT analysis_id FROM stock_analysis 
            WHERE ticker = ? 
            ORDER BY analysis_date DESC 
            LIMIT 1
        """, (ticker,))
        
        result = cursor.fetchone()
        analysis_id = result[0] if result else None
        
        cursor.execute("""
            INSERT INTO trade_log (
                analysis_id, ticker, entry_date, entry_price, position_size,
                strategy_type, option_type, strikes, expiration, contracts, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            analysis_id, ticker, entry_date, entry_price, position_size,
            strategy_type, option_type, strikes, expiration, contracts, notes
        ))
        
        trade_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return trade_id
    
    def close_trade(self, trade_id: int, exit_date: str, exit_price: float,
                    pnl: float = None, pnl_pct: float = None):
        """Close a trade and record P&L"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE trade_log 
            SET exit_date = ?, exit_price = ?, pnl = ?, pnl_pct = ?
            WHERE trade_id = ?
        """, (exit_date, exit_price, pnl, pnl_pct, trade_id))
        
        conn.commit()
        conn.close()
    
    def get_historical_performance(self, ticker: str = None, 
                                   days_back: int = 30) -> List[Dict]:
        """Get historical analysis for a ticker or all tickers"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = """
            SELECT 
                sa.analysis_date,
                sa.ticker,
                sa.total_score,
                sa.price,
                ca.recommendation,
                ca.sentiment_score,
                ca.catalyst_score_claude,
                ca.risk_score
            FROM stock_analysis sa
            LEFT JOIN claude_analysis ca ON sa.analysis_id = ca.analysis_id
            WHERE sa.analysis_date >= date('now', '-' || ? || ' days')
        """
        
        params = [days_back]
        
        if ticker:
            query += " AND sa.ticker = ?"
            params.append(ticker)
        
        query += " ORDER BY sa.analysis_date DESC, sa.total_score DESC"
        
        cursor.execute(query, params)
        
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def get_summary_stats(self, days_back: int = 30) -> Dict:
        """Get summary statistics for recent analyses"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total runs
        cursor.execute("""
            SELECT COUNT(*) FROM analysis_runs
            WHERE run_date >= date('now', '-' || ? || ' days')
        """, (days_back,))
        total_runs = cursor.fetchone()[0]
        
        # Total stocks analyzed
        cursor.execute("""
            SELECT COUNT(*) FROM stock_analysis
            WHERE analysis_date >= date('now', '-' || ? || ' days')
        """, (days_back,))
        total_stocks = cursor.fetchone()[0]
        
        # Average score
        cursor.execute("""
            SELECT AVG(total_score) FROM stock_analysis
            WHERE analysis_date >= date('now', '-' || ? || ' days')
        """, (days_back,))
        avg_score = cursor.fetchone()[0]
        
        # Recommendation distribution
        cursor.execute("""
            SELECT ca.recommendation, COUNT(*) as count
            FROM claude_analysis ca
            JOIN stock_analysis sa ON ca.analysis_id = sa.analysis_id
            WHERE sa.analysis_date >= date('now', '-' || ? || ' days')
            GROUP BY ca.recommendation
        """, (days_back,))
        recommendations = dict(cursor.fetchall())
        
        # Trade statistics (if any trades logged)
        cursor.execute("""
            SELECT 
                COUNT(*) as total_trades,
                COUNT(exit_date) as closed_trades,
                AVG(pnl_pct) as avg_pnl_pct,
                SUM(CASE WHEN pnl > 0 THEN 1 ELSE 0 END) as winners,
                SUM(CASE WHEN pnl < 0 THEN 1 ELSE 0 END) as losers
            FROM trade_log
            WHERE entry_date >= date('now', '-' || ? || ' days')
        """, (days_back,))
        
        trade_stats = cursor.fetchone()
        
        conn.close()
        
        return {
            'total_runs': total_runs,
            'total_stocks_analyzed': total_stocks,
            'average_score': round(avg_score, 2) if avg_score else 0,
            'recommendations': recommendations,
            'trades': {
                'total': trade_stats[0],
                'closed': trade_stats[1],
                'avg_pnl_pct': round(trade_stats[2], 2) if trade_stats[2] else 0,
                'winners': trade_stats[3] or 0,
                'losers': trade_stats[4] or 0,
                'win_rate': round((trade_stats[3] or 0) / max(trade_stats[1] or 1, 1) * 100, 1)
            }
        }
    
    def export_to_csv(self, output_path: str, days_back: int = 30):
        """Export historical data to CSV for external analysis"""
        conn = sqlite3.connect(self.db_path)
        
        query = """
            SELECT 
                sa.*,
                ca.sentiment_score,
                ca.sentiment_label,
                ca.catalyst_score_claude,
                ca.risk_score,
                ca.risk_label,
                ca.recommendation,
                ca.confidence,
                ca.position_size,
                ca.stronger_case,
                ca.conviction_level
            FROM stock_analysis sa
            LEFT JOIN claude_analysis ca ON sa.analysis_id = ca.analysis_id
            WHERE sa.analysis_date >= date('now', '-' || ? || ' days')
            ORDER BY sa.analysis_date DESC, sa.total_score DESC
        """
        
        import pandas as pd
        df = pd.read_sql_query(query, conn, params=(days_back,))
        df.to_csv(output_path, index=False)
        
        conn.close()
        print(f"✅ Exported {len(df)} records to {output_path}")
