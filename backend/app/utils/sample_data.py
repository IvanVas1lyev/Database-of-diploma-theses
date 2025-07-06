from sqlalchemy.orm import Session
from ..models.thesis import Student
from ..core.database import SessionLocal

SAMPLE_STUDENTS = [
    {
        "name": "Alice Johnson",
        "graduation_year": 2024,
        "thesis_title": "Machine Learning Applications in Financial Risk Assessment",
        "thesis_summary": "This thesis explores the application of various machine learning algorithms to assess financial risk in banking institutions. The study compares traditional statistical methods with modern ML approaches including random forests, neural networks, and gradient boosting. Results show significant improvements in risk prediction accuracy using ensemble methods.",
        "python_code": """# Calculate portfolio risk using Monte Carlo simulation
import random
import math

def calculate_portfolio_risk(returns, weights, num_simulations=1000):
    \"\"\"
    Calculate portfolio risk using Monte Carlo simulation
    Args: returns (list), weights (list), num_simulations (int)
    \"\"\"
    if not args:
        returns = [0.08, 0.12, 0.06]
        weights = [0.4, 0.4, 0.2]
        num_simulations = 1000
    else:
        returns = [float(x) for x in args[0].split()]
        weights = [float(x) for x in args[1].split()]
        num_simulations = int(args[2]) if len(args) > 2 else 1000
    
    portfolio_returns = []
    for _ in range(num_simulations):
        portfolio_return = sum(r * w * random.gauss(1, 0.1) for r, w in zip(returns, weights))
        portfolio_returns.append(portfolio_return)
    
    mean_return = sum(portfolio_returns) / len(portfolio_returns)
    variance = sum((r - mean_return) ** 2 for r in portfolio_returns) / len(portfolio_returns)
    risk = math.sqrt(variance)
    
    print(f"Expected Return: {mean_return:.4f}")
    print(f"Portfolio Risk (Std Dev): {risk:.4f}")
    print(f"Risk-Return Ratio: {risk/mean_return:.4f}")
    
    return {"return": mean_return, "risk": risk}

calculate_portfolio_risk([], [], 1000)"""
    },
    {
        "name": "Bob Chen",
        "graduation_year": 2024,
        "thesis_title": "Bayesian Analysis of Climate Change Data",
        "thesis_summary": "A comprehensive Bayesian statistical analysis of global temperature data spanning the last century. The research employs hierarchical Bayesian models to account for spatial and temporal correlations in climate data. The study provides probabilistic forecasts for future temperature trends and quantifies uncertainty in climate projections.",
        "python_code": """# Bayesian temperature trend analysis
import math
import random

def bayesian_temperature_analysis(temperatures, years):
    \"\"\"
    Simple Bayesian linear regression for temperature trends
    Args: temperatures (list), years (list)
    \"\"\"
    if not args:
        # Sample temperature data (Celsius anomalies)
        temperatures = [-0.2, 0.1, 0.3, 0.5, 0.8, 1.0, 1.2, 1.1, 1.3, 1.5]
        years = list(range(2015, 2025))
    else:
        temperatures = [float(x) for x in args[0].split(',')]
        years = [int(x) for x in args[1].split(',')]
    
    n = len(temperatures)
    mean_year = sum(years) / n
    mean_temp = sum(temperatures) / n
    
    # Calculate slope (trend)
    numerator = sum((years[i] - mean_year) * (temperatures[i] - mean_temp) for i in range(n))
    denominator = sum((years[i] - mean_year) ** 2 for i in range(n))
    slope = numerator / denominator
    
    # Calculate intercept
    intercept = mean_temp - slope * mean_year
    
    # Calculate R-squared
    ss_res = sum((temperatures[i] - (slope * years[i] + intercept)) ** 2 for i in range(n))
    ss_tot = sum((temperatures[i] - mean_temp) ** 2 for i in range(n))
    r_squared = 1 - (ss_res / ss_tot)
    
    print(f"Temperature Trend: {slope:.4f}°C per year")
    print(f"R-squared: {r_squared:.4f}")
    print(f"Projected 2030 temperature anomaly: {slope * 2030 + intercept:.2f}°C")
    
    return {"slope": slope, "r_squared": r_squared}

bayesian_temperature_analysis([], [])"""
    },
    {
        "name": "Carol Davis",
        "graduation_year": 2023,
        "thesis_title": "Statistical Methods for Social Media Sentiment Analysis",
        "thesis_summary": "This research develops novel statistical approaches for analyzing sentiment in social media data. The study combines traditional text mining techniques with advanced statistical models to handle the challenges of informal language, sarcasm, and context-dependent sentiment. Applications include brand monitoring and public opinion analysis.",
        "python_code": """# Sentiment analysis with statistical confidence intervals
import math

def sentiment_confidence_analysis(positive_count, total_count, confidence_level=0.95):
    \"\"\"
    Calculate sentiment score with confidence intervals
    Args: positive_count (int), total_count (int), confidence_level (float)
    \"\"\"
    if not args:
        positive_count = 750
        total_count = 1000
        confidence_level = 0.95
    else:
        positive_count = int(args[0])
        total_count = int(args[1])
        confidence_level = float(args[2]) if len(args) > 2 else 0.95
    
    # Calculate proportion
    p = positive_count / total_count
    
    # Calculate standard error
    se = math.sqrt(p * (1 - p) / total_count)
    
    # Z-score for confidence level (approximation)
    z_scores = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
    z = z_scores.get(confidence_level, 1.96)
    
    # Confidence interval
    margin_error = z * se
    ci_lower = p - margin_error
    ci_upper = p + margin_error
    
    print(f"Sentiment Score: {p:.3f} ({p*100:.1f}% positive)")
    print(f"{confidence_level*100:.0f}% Confidence Interval: [{ci_lower:.3f}, {ci_upper:.3f}]")
    print(f"Margin of Error: ±{margin_error:.3f}")
    print(f"Sample Size: {total_count}")
    
    return {"sentiment": p, "ci_lower": ci_lower, "ci_upper": ci_upper}

sentiment_confidence_analysis(750, 1000, 0.95)"""
    },
    {
        "name": "David Wilson",
        "graduation_year": 2023,
        "thesis_title": "Time Series Analysis of Economic Indicators",
        "thesis_summary": "An in-depth statistical analysis of key economic indicators using advanced time series methods. The research applies ARIMA models, seasonal decomposition, and cointegration analysis to understand relationships between GDP, inflation, and unemployment. The study provides insights for economic forecasting and policy analysis.",
        "python_code": """# Economic indicator correlation analysis
import math

def economic_correlation_analysis(gdp_growth, inflation, unemployment):
    \"\"\"
    Analyze correlations between economic indicators
    Args: gdp_growth (list), inflation (list), unemployment (list)
    \"\"\"
    if not args:
        gdp_growth = [2.1, 2.3, 1.8, 2.5, 2.0, 1.9, 2.4, 2.2]
        inflation = [1.5, 1.8, 2.1, 2.3, 2.0, 1.7, 1.9, 2.2]
        unemployment = [5.2, 4.8, 5.1, 4.5, 4.9, 5.0, 4.7, 4.6]
    else:
        gdp_growth = [float(x) for x in args[0].split(',')]
        inflation = [float(x) for x in args[1].split(',')]
        unemployment = [float(x) for x in args[2].split(',')]
    
    n = len(gdp_growth)
    
    def correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x)))
        sum_sq_x = sum((x[i] - mean_x) ** 2 for i in range(len(x)))
        sum_sq_y = sum((y[i] - mean_y) ** 2 for i in range(len(y)))
        
        denominator = math.sqrt(sum_sq_x * sum_sq_y)
        return numerator / denominator if denominator != 0 else 0
    
    corr_gdp_inflation = correlation(gdp_growth, inflation)
    corr_gdp_unemployment = correlation(gdp_growth, unemployment)
    corr_inflation_unemployment = correlation(inflation, unemployment)
    
    print(f"GDP Growth vs Inflation: r = {corr_gdp_inflation:.3f}")
    print(f"GDP Growth vs Unemployment: r = {corr_gdp_unemployment:.3f}")
    print(f"Inflation vs Unemployment: r = {corr_inflation_unemployment:.3f}")
    
    print(f"\\nMean GDP Growth: {sum(gdp_growth)/n:.2f}%")
    print(f"Mean Inflation: {sum(inflation)/n:.2f}%")
    print(f"Mean Unemployment: {sum(unemployment)/n:.2f}%")
    
    return {
        "gdp_inflation_corr": corr_gdp_inflation,
        "gdp_unemployment_corr": corr_gdp_unemployment,
        "inflation_unemployment_corr": corr_inflation_unemployment
    }

economic_correlation_analysis([], [], [])"""
    },
    {
        "name": "Emma Thompson",
        "graduation_year": 2022,
        "thesis_title": "Statistical Quality Control in Manufacturing",
        "thesis_summary": "This thesis develops advanced statistical process control methods for modern manufacturing environments. The research focuses on multivariate control charts, capability analysis, and real-time monitoring systems. Applications include automotive and pharmaceutical manufacturing with emphasis on Six Sigma methodologies.",
        "python_code": """# Statistical Process Control Analysis
import math

def process_capability_analysis(measurements, lower_spec, upper_spec):
    \"\"\"
    Calculate process capability indices (Cp, Cpk)
    Args: measurements (list), lower_spec (float), upper_spec (float)
    \"\"\"
    if not args:
        measurements = [10.2, 10.1, 9.9, 10.3, 10.0, 9.8, 10.4, 10.1, 9.9, 10.2]
        lower_spec = 9.5
        upper_spec = 10.5
    else:
        measurements = [float(x) for x in args[0].split(',')]
        lower_spec = float(args[1])
        upper_spec = float(args[2])
    
    n = len(measurements)
    mean = sum(measurements) / n
    
    # Calculate standard deviation
    variance = sum((x - mean) ** 2 for x in measurements) / (n - 1)
    std_dev = math.sqrt(variance)
    
    # Process capability indices
    cp = (upper_spec - lower_spec) / (6 * std_dev)
    cpu = (upper_spec - mean) / (3 * std_dev)
    cpl = (mean - lower_spec) / (3 * std_dev)
    cpk = min(cpu, cpl)
    
    # Defect rate estimation (parts per million)
    z_upper = (upper_spec - mean) / std_dev
    z_lower = (mean - lower_spec) / std_dev
    
    print(f"Process Mean: {mean:.3f}")
    print(f"Process Std Dev: {std_dev:.3f}")
    print(f"Cp (Process Capability): {cp:.3f}")
    print(f"Cpk (Process Capability Index): {cpk:.3f}")
    
    if cpk >= 1.33:
        print("Process is CAPABLE (Cpk ≥ 1.33)")
    elif cpk >= 1.0:
        print("Process is MARGINALLY CAPABLE (1.0 ≤ Cpk < 1.33)")
    else:
        print("Process is NOT CAPABLE (Cpk < 1.0)")
    
    return {"cp": cp, "cpk": cpk, "mean": mean, "std_dev": std_dev}

process_capability_analysis([], 9.5, 10.5)"""
    },
    {
        "name": "Frank Rodriguez",
        "graduation_year": 2022,
        "thesis_title": "Survival Analysis in Medical Statistics",
        "thesis_summary": "A comprehensive study of survival analysis methods applied to clinical trial data. The research compares Kaplan-Meier estimators, Cox proportional hazards models, and parametric survival models. Applications include cancer treatment efficacy and drug development with focus on censored data handling.",
        "python_code": """# Kaplan-Meier Survival Analysis
import math

def kaplan_meier_analysis(survival_times, events):
    \"\"\"
    Calculate Kaplan-Meier survival probabilities
    Args: survival_times (list), events (list of 0/1 for censored/event)
    \"\"\"
    if not args:
        survival_times = [5, 8, 12, 15, 18, 22, 25, 30, 35, 40]
        events = [1, 1, 0, 1, 1, 0, 1, 1, 0, 1]  # 1=event, 0=censored
    else:
        survival_times = [float(x) for x in args[0].split(',')]
        events = [int(x) for x in args[1].split(',')]
    
    # Combine and sort data
    data = list(zip(survival_times, events))
    data.sort()
    
    n_at_risk = len(data)
    survival_prob = 1.0
    
    print("Time\\tEvents\\tAt Risk\\tSurvival Prob")
    print("-" * 40)
    
    results = []
    
    for i, (time, event) in enumerate(data):
        if event == 1:  # Event occurred
            survival_prob *= (n_at_risk - 1) / n_at_risk
            print(f"{time:.1f}\\t{event}\\t{n_at_risk}\\t{survival_prob:.3f}")
            results.append((time, survival_prob))
        
        n_at_risk -= 1
    
    # Calculate median survival time
    median_survival = None
    for time, prob in results:
        if prob <= 0.5:
            median_survival = time
            break
    
    print(f"\\nMedian Survival Time: {median_survival if median_survival else 'Not reached'}")
    print(f"Final Survival Probability: {survival_prob:.3f}")
    
    return {"final_survival": survival_prob, "median_survival": median_survival}

kaplan_meier_analysis([], [])"""
    }
]


def create_sample_data():
    """Create sample students in the database"""
    db = SessionLocal()
    try:
        # Check if data already exists
        existing_count = db.query(Student).count()
        if existing_count > 0:
            print(f"Sample data already exists ({existing_count} students)")
            return
        
        # Create sample students
        for student_data in SAMPLE_STUDENTS:
            student = Student(**student_data)
            db.add(student)
        
        db.commit()
        print(f"Created {len(SAMPLE_STUDENTS)} sample students")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_data()