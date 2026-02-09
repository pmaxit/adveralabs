"""Website views."""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import json


def home(request):
    """Home page view."""
    context = {
        'page_title': 'Advera Labs - AI-Powered Cross-Channel Ad Optimization',
    }
    return render(request, 'website/home.html', context)


@require_http_methods(["POST"])
def calculate_roi(request):
    """Calculate ROI based on user input."""
    try:
        # Handle both form data and JSON
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            monthly_spend = float(data.get('monthly_spend', 100000))
            current_roas = float(data.get('current_roas', 3.0))
        else:
            monthly_spend = float(request.POST.get('monthly_spend', 100000))
            current_roas = float(request.POST.get('current_roas', 3.0))
        
        # Calculate potential savings (10-20% of spend)
        wasted_spend_percentage = 0.15  # Average of 10-20%
        potential_savings = monthly_spend * wasted_spend_percentage
        
        return JsonResponse({
            'success': True,
            'savings': round(potential_savings, 2),
            'formatted_savings': f"${potential_savings:,.0f}"
        })
    except (ValueError, TypeError) as e:
        return JsonResponse({
            'success': False,
            'error': 'Invalid input values'
        }, status=400)


def about(request):
    """About page view."""
    context = {
        'page_title': 'About Us - Advera Labs',
    }
    return render(request, 'website/about.html', context)


def blog(request):
    """Blog list page view."""
    # Sample blog posts - in production, these would come from a database
    blog_posts = [
        {
            'id': 7,
            'title': 'Multi-Armed Bandit Algorithms in Advertising: A 2025 Research Review',
            'excerpt': 'Deep dive into the latest research on MAB algorithms for ad optimization, including comparative studies and real-world applications.',
            'author': 'Dr. Sarah Chen',
            'date': '2025-01-31',
            'category': 'Research',
            'read_time': '12 min read',
            'image': 'blog-7.jpg',
            'featured': True
        },
        {
            'id': 8,
            'title': 'Combinatorial Bandits for Multichannel Budget Optimization: Breaking Down the Latest Research',
            'excerpt': 'Understanding how combinatorial bandit algorithms solve the complex problem of allocating budgets across multiple advertising channels simultaneously.',
            'author': 'Michael Park',
            'date': '2025-01-28',
            'category': 'Research',
            'read_time': '15 min read',
            'image': 'blog-8.jpg',
            'featured': True
        },
        {
            'id': 9,
            'title': 'Bayesian Multi-Armed Bandits: The Science Behind Smarter Ad Recommendations',
            'excerpt': 'Exploring how Bayesian approaches to multi-armed bandits provide probabilistic reasoning for ad optimization decisions.',
            'author': 'David Kim',
            'date': '2025-01-25',
            'category': 'Research',
            'read_time': '11 min read',
            'image': 'blog-9.jpg'
        },
        {
            'id': 10,
            'title': 'Reinforcement Learning Meets Advertising: A Practical Guide to RL-Based Optimization',
            'excerpt': 'How reinforcement learning algorithms are revolutionizing ad selection and budget allocation in digital marketing.',
            'author': 'Dr. Emily Rodriguez',
            'date': '2025-01-22',
            'category': 'Research',
            'read_time': '14 min read',
            'image': 'blog-10.jpg'
        },
        {
            'id': 1,
            'title': 'Why LTV-Based Optimization Beats ROAS Every Time',
            'excerpt': 'Learn how optimizing for lifetime value instead of return on ad spend can increase your profit margins by 20-30%.',
            'author': 'Sarah Chen',
            'date': '2025-01-15',
            'category': 'Optimization',
            'read_time': '5 min read',
            'image': 'blog-1.jpg'
        },
        {
            'id': 2,
            'title': 'The Hidden Cost of Misconfigured Conversion Tracking',
            'excerpt': 'Discover how broken tracking and misconfigured conversions are silently draining 10-20% of your ad budget.',
            'author': 'Michael Park',
            'date': '2025-01-10',
            'category': 'Tracking',
            'read_time': '7 min read',
            'image': 'blog-2.jpg'
        },
        {
            'id': 3,
            'title': 'Cross-Channel Budget Allocation: A Complete Guide',
            'excerpt': 'Master the art of allocating budgets across Facebook and Google Ads for maximum unified ROI.',
            'author': 'David Kim',
            'date': '2025-01-05',
            'category': 'Strategy',
            'read_time': '10 min read',
            'image': 'blog-3.jpg'
        },
        {
            'id': 4,
            'title': 'How We Recovered $50K in Wasted Ad Spend for a DTC Brand',
            'excerpt': 'Case study: How Advera Labs helped a $500K/month e-commerce brand recover wasted spend and improve margins.',
            'author': 'Emily Rodriguez',
            'date': '2024-12-28',
            'category': 'Case Study',
            'read_time': '8 min read',
            'image': 'blog-4.jpg'
        },
        {
            'id': 5,
            'title': 'Smart Signal Generation: Feeding Platforms Better Data',
            'excerpt': 'Learn how to send high-quality conversion signals to Meta and Google to unlock the full potential of Smart Bidding.',
            'author': 'James Wilson',
            'date': '2024-12-20',
            'category': 'Technical',
            'read_time': '6 min read',
            'image': 'blog-5.jpg'
        },
        {
            'id': 6,
            'title': 'Incrementality Testing: Proving Your Optimization Works',
            'excerpt': 'Why A/B tests and geo holdouts are essential for validating ad optimization tools and showing real incremental lift.',
            'author': 'Lisa Anderson',
            'date': '2024-12-15',
            'category': 'Testing',
            'read_time': '9 min read',
            'image': 'blog-6.jpg'
        },
    ]
    
    context = {
        'page_title': 'Blog - Advera Labs',
        'blog_posts': blog_posts,
    }
    return render(request, 'website/blog.html', context)


def blog_post(request, post_id):
    """Individual blog post view."""
    # Sample blog posts data
    posts_data = {
        7: {
            'title': 'Multi-Armed Bandit Algorithms in Advertising: A 2025 Research Review',
            'author': 'Dr. Sarah Chen',
            'date': '2025-01-31',
            'category': 'Research',
            'read_time': '12 min read',
            'has_animations': True,
            'has_research_papers': True,
            'content': '''
            <div class="research-intro">
                <p class="lead">Multi-armed bandit (MAB) algorithms have emerged as one of the most powerful frameworks for optimizing advertising decisions in real-time. As the digital advertising market approaches $700 billion globally, understanding these algorithms isn't just academic—it's essential for competitive advantage.</p>
                <p>This article synthesizes the latest research from 2024-2025, breaking down complex algorithms into actionable insights for performance marketers and industry leaders.</p>
            </div>

            <h2>What Are Multi-Armed Bandit Algorithms?</h2>
            <p>Imagine you're at a casino with multiple slot machines (arms), each with an unknown probability of winning. Your goal: maximize your winnings by figuring out which machines pay out the most, while still exploring new machines that might be better.</p>
            
            <div class="animated-diagram">
                <div class="bandit-visualization">
                    <div class="bandit-arm" data-arm="1">
                        <div class="arm-machine">🎰</div>
                        <div class="arm-stats">
                            <span class="stat-label">Win Rate:</span>
                            <span class="stat-value" data-value="0.65">65%</span>
                        </div>
                    </div>
                    <div class="bandit-arm" data-arm="2">
                        <div class="arm-machine">🎰</div>
                        <div class="arm-stats">
                            <span class="stat-label">Win Rate:</span>
                            <span class="stat-value" data-value="0.45">45%</span>
                        </div>
                    </div>
                    <div class="bandit-arm" data-arm="3">
                        <div class="arm-machine">🎰</div>
                        <div class="arm-stats">
                            <span class="stat-label">Win Rate:</span>
                            <span class="stat-value" data-value="0.80">80%</span>
                        </div>
                    </div>
                </div>
                <p class="diagram-caption">In advertising, each "arm" represents a different campaign, ad set, or creative. The algorithm learns which performs best while balancing exploration (trying new options) and exploitation (using what works).</p>
            </div>

            <h2>The Exploration-Exploitation Tradeoff</h2>
            <p>This is the core challenge MAB algorithms solve: <strong>exploration</strong> (trying new options to learn) vs. <strong>exploitation</strong> (using what you know works).</p>
            
            <div class="comparison-table">
                <table>
                    <thead>
                        <tr>
                            <th>Strategy</th>
                            <th>Approach</th>
                            <th>Best For</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Pure Exploration</strong></td>
                            <td>Test everything equally</td>
                            <td>Early stages, new campaigns</td>
                        </tr>
                        <tr>
                            <td><strong>Pure Exploitation</strong></td>
                            <td>Only use best-known option</td>
                            <td>Mature campaigns, limited budget</td>
                        </tr>
                        <tr>
                            <td><strong>MAB Algorithms</strong></td>
                            <td>Balance both dynamically</td>
                            <td>Real-world optimization</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <h2>Key MAB Algorithms: A Comparative Analysis</h2>
            <p>Recent research has compared multiple MAB algorithms in advertising contexts. Here's what the data shows:</p>

            <h3>1. Epsilon-Greedy</h3>
            <p>The simplest approach: with probability ε (epsilon), explore randomly; otherwise, exploit the best-known option.</p>
            <div class="algorithm-box">
                <strong>Pros:</strong> Simple, interpretable, works well with sufficient data<br>
                <strong>Cons:</strong> Fixed exploration rate, doesn't adapt to uncertainty<br>
                <strong>Performance:</strong> Baseline algorithm, often outperformed by more sophisticated methods
            </div>

            <h3>2. Upper Confidence Bound (UCB)</h3>
            <p>UCB selects arms based on both their average reward and uncertainty. It chooses arms with high potential (high average + high uncertainty).</p>
            <div class="algorithm-box">
                <strong>Pros:</strong> Theoretically optimal, adapts to uncertainty<br>
                <strong>Cons:</strong> Requires assumptions about reward distribution<br>
                <strong>Performance:</strong> Strong theoretical guarantees, good in practice
            </div>

            <h3>3. Thompson Sampling</h3>
            <p>A Bayesian approach that maintains probability distributions over arm rewards and samples from them proportionally.</p>
            <div class="algorithm-box">
                <strong>Pros:</strong> Excellent empirical performance, naturally handles uncertainty<br>
                <strong>Cons:</strong> Computationally more expensive<br>
                <strong>Performance:</strong> Often outperforms UCB in practice, widely used in production
            </div>

            <h3>4. Adaptive Algorithms</h3>
            <p>Recent research (2024-2025) has focused on adaptive algorithms that switch strategies based on data volume and campaign maturity.</p>
            <div class="algorithm-box">
                <strong>Pros:</strong> Best of both worlds, adapts to campaign lifecycle<br>
                <strong>Cons:</strong> More complex to implement<br>
                <strong>Performance:</strong> Shows promise in recent studies
            </div>

            <h2>Real-World Performance: What Research Shows</h2>
            <p>A 2024 comparative study by Zhao et al. evaluated multiple MAB algorithms in advertising recommendation systems. Key findings:</p>
            
            <div class="research-findings">
                <div class="finding-card">
                    <div class="finding-icon">📊</div>
                    <h4>Thompson Sampling Leads</h4>
                    <p>Outperformed other algorithms by 12-18% in conversion rate optimization scenarios.</p>
                </div>
                <div class="finding-card">
                    <div class="finding-icon">⚡</div>
                    <h4>UCB for Cold Starts</h4>
                    <p>Performed best in early campaign stages with limited data (first 1,000 impressions).</p>
                </div>
                <div class="finding-card">
                    <div class="finding-icon">🎯</div>
                    <h4>Adaptive Wins Overall</h4>
                    <p>Adaptive algorithms combining multiple strategies showed 20-25% improvement over single-strategy approaches.</p>
                </div>
            </div>

            <h2>Implementation Considerations for Marketers</h2>
            <p>While the theory is elegant, practical implementation requires attention to several factors:</p>
            
            <h3>Data Requirements</h3>
            <ul>
                <li><strong>Minimum sample size:</strong> Most algorithms need at least 100-1,000 impressions per arm to be reliable</li>
                <li><strong>Conversion volume:</strong> Low conversion rates require longer learning periods</li>
                <li><strong>Data quality:</strong> Tracking issues can severely degrade algorithm performance</li>
            </ul>

            <h3>Budget Constraints</h3>
            <p>MAB algorithms work best when you have flexibility to shift budgets. Fixed budgets require constrained bandit algorithms, which are more complex.</p>

            <h3>Platform Integration</h3>
            <p>Most ad platforms (Meta, Google) use their own optimization algorithms. MAB algorithms are most valuable when:</p>
            <ul>
                <li>Optimizing across platforms (cross-channel coordination)</li>
                <li>Platform algorithms aren't performing well</li>
                <li>You need business-level optimization (profit, LTV) beyond platform metrics</li>
            </ul>

            <h2>The Future: Combinatorial and Contextual Bandits</h2>
            <p>Recent research (2025) is exploring more sophisticated variants:</p>
            
            <h3>Combinatorial Bandits</h3>
            <p>For multichannel advertising, where you're selecting combinations of campaigns across platforms simultaneously. A 2025 paper by Gangopadhyay et al. shows these can improve cross-channel ROI by 15-30%.</p>

            <h3>Contextual Bandits</h3>
            <p>Algorithms that use user context (demographics, behavior) to make better decisions. These are becoming standard in programmatic advertising.</p>

            <h2>Key Takeaways for Industry Leaders</h2>
            <div class="takeaways">
                <div class="takeaway-item">
                    <span class="takeaway-number">1</span>
                    <div>
                        <h4>MAB algorithms aren't just academic—they're production-ready</h4>
                        <p>Major platforms and ad tech companies use variants of these algorithms. Understanding them helps you work with, not against, platform optimization.</p>
                    </div>
                </div>
                <div class="takeaway-item">
                    <span class="takeaway-number">2</span>
                    <div>
                        <h4>Thompson Sampling is the current state-of-the-art</h4>
                        <p>For most use cases, Thompson Sampling provides the best balance of performance and interpretability.</p>
                    </div>
                </div>
                <div class="takeaway-item">
                    <span class="takeaway-number">3</span>
                    <div>
                        <h4>Adaptive algorithms are the future</h4>
                        <p>Research shows adaptive approaches that combine multiple strategies outperform single-strategy algorithms.</p>
                    </div>
                </div>
                <div class="takeaway-item">
                    <span class="takeaway-number">4</span>
                    <div>
                        <h4>Data quality is critical</h4>
                        <p>No algorithm can overcome poor tracking or misconfigured conversions. Fix data issues first.</p>
                    </div>
                </div>
            </div>

            <h2>Research Papers & Further Reading</h2>
            <div class="research-papers">
                <div class="paper-card">
                    <h4>Comparison of multi-armed bandit algorithms in advertising recommendation systems</h4>
                    <p class="paper-authors">J. Zhao - Applied and Computational Engineering, 2024</p>
                    <p class="paper-abstract">Comprehensive comparison of MAB algorithms in real advertising systems.</p>
                    <a href="https://ace.ewapub.com/article/view/15915" target="_blank" class="paper-link">Read Paper →</a>
                </div>
                <div class="paper-card">
                    <h4>Harnessing Multi-Armed Bandits for Smarter Digital Marketing Decisions</h4>
                    <p class="paper-authors">S. Agarwal, G. Paliwal, S.B. Peta, S. Panyam - Sch J Eng Tech, 2024</p>
                    <p class="paper-abstract">Practical guide to MAB algorithms in digital marketing contexts.</p>
                    <a href="https://saspublishers.com/media/articles/SJET_1210_307-313.pdf" target="_blank" class="paper-link">Read Paper →</a>
                </div>
                <div class="paper-card">
                    <h4>Utilizing reinforcement learning bandit algorithms in advertising optimization</h4>
                    <p class="paper-authors">S. Zhang - Highlights in Science, Engineering and Technology, 2024</p>
                    <p class="paper-abstract">Explores RL-based approaches to bandit problems in advertising.</p>
                    <a href="https://pdfs.semanticscholar.org/14b1/b97f36bb01333e6863a60c781373f6cba906.pdf" target="_blank" class="paper-link">Read Paper →</a>
                </div>
                <div class="paper-card">
                    <h4>Bandit Algorithms for Advertising Optimization: A Comparative Study</h4>
                    <p class="paper-authors">Z. Tian - ITM Web of Conferences, 2025</p>
                    <p class="paper-abstract">Recent comparative analysis of bandit algorithms in advertising.</p>
                    <a href="https://www.itm-conferences.org/articles/itmconf/abs/2025/04/itmconf_iwadi2024_01019/itmconf_iwadi2024_01019.html" target="_blank" class="paper-link">Read Paper →</a>
                </div>
                <div class="paper-card">
                    <h4>Adaptive Budget Optimization for Multichannel Advertising Using Combinatorial Bandits</h4>
                    <p class="paper-authors">B. Gangopadhyay, Z. Wang, A.S. Chiappa - arXiv, 2025</p>
                    <p class="paper-abstract">Cutting-edge research on combinatorial bandits for cross-channel optimization.</p>
                    <a href="https://arxiv.org/abs/2502.02920" target="_blank" class="paper-link">Read Paper →</a>
                </div>
            </div>

            <div class="cta-box">
                <h3>Ready to Implement MAB Algorithms in Your Advertising?</h3>
                <p>Advera Labs uses state-of-the-art multi-armed bandit algorithms to optimize your ad spend across Facebook and Google. See how we can help you leverage these techniques.</p>
                <a href="/#demo" class="btn-primary">Start Free Trial</a>
            </div>
            '''
        },
        8: {
            'title': 'Combinatorial Bandits for Multichannel Budget Optimization: Breaking Down the Latest Research',
            'author': 'Michael Park',
            'date': '2025-01-28',
            'category': 'Research',
            'read_time': '15 min read',
            'has_animations': True,
            'has_research_papers': True,
            'content': '''
            <div class="research-intro">
                <p class="lead">As brands increasingly advertise across multiple channels simultaneously, a new challenge emerges: how do you optimize budget allocation when you're selecting combinations of campaigns, not just individual ones?</p>
                <p>This is where <strong>combinatorial bandits</strong> come in—a cutting-edge extension of multi-armed bandit algorithms that's showing remarkable results in recent research.</p>
            </div>

            <h2>The Multichannel Challenge</h2>
            <p>Traditional multi-armed bandit algorithms assume you're selecting one arm at a time. But in real-world advertising:</p>
            <ul>
                <li>You're running campaigns on Facebook, Google, LinkedIn, and more simultaneously</li>
                <li>Each channel has multiple campaigns, ad sets, and creatives</li>
                <li>You need to allocate a fixed budget across all of them</li>
                <li>Performance depends on the combination, not just individual components</li>
            </ul>

            <div class="animated-diagram">
                <div class="multichannel-visualization">
                    <div class="channel-group" data-channel="facebook">
                        <h4>Facebook Ads</h4>
                        <div class="campaigns">
                            <div class="campaign" data-id="fb1">Campaign A</div>
                            <div class="campaign" data-id="fb2">Campaign B</div>
                            <div class="campaign" data-id="fb3">Campaign C</div>
                        </div>
                    </div>
                    <div class="channel-group" data-channel="google">
                        <h4>Google Ads</h4>
                        <div class="campaigns">
                            <div class="campaign" data-id="gg1">Campaign X</div>
                            <div class="campaign" data-id="gg2">Campaign Y</div>
                        </div>
                    </div>
                    <div class="budget-allocation">
                        <div class="budget-bar">
                            <div class="budget-segment" data-campaign="fb1" style="width: 20%"></div>
                            <div class="budget-segment" data-campaign="fb2" style="width: 15%"></div>
                            <div class="budget-segment" data-campaign="fb3" style="width: 10%"></div>
                            <div class="budget-segment" data-campaign="gg1" style="width: 35%"></div>
                            <div class="budget-segment" data-campaign="gg2" style="width: 20%"></div>
                        </div>
                        <p class="diagram-caption">Combinatorial bandits optimize the entire budget allocation simultaneously, considering interactions between campaigns.</p>
                    </div>
                </div>
            </div>

            <h2>What Are Combinatorial Bandits?</h2>
            <p>Combinatorial bandits extend the multi-armed bandit framework to handle <strong>subset selection</strong> problems. Instead of choosing one arm, you select a combination (subset) of arms, and the reward depends on the entire combination.</p>

            <h3>Key Differences from Standard MAB</h3>
            <div class="comparison-table">
                <table>
                    <thead>
                        <tr>
                            <th>Aspect</th>
                            <th>Standard MAB</th>
                            <th>Combinatorial Bandits</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Selection</strong></td>
                            <td>One arm at a time</td>
                            <td>Subset of arms simultaneously</td>
                        </tr>
                        <tr>
                            <td><strong>Reward</strong></td>
                            <td>Independent per arm</td>
                            <td>Depends on combination</td>
                        </tr>
                        <tr>
                            <td><strong>Complexity</strong></td>
                            <td>O(n) - linear</td>
                            <td>O(2^n) - exponential (requires approximation)</td>
                        </tr>
                        <tr>
                            <td><strong>Best For</strong></td>
                            <td>Single campaign optimization</td>
                            <td>Cross-channel budget allocation</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <h2>Latest Research: Gangopadhyay et al. (2025)</h2>
            <p>A groundbreaking 2025 paper from researchers at leading institutions introduces an adaptive combinatorial bandit algorithm specifically designed for multichannel advertising.</p>

            <h3>Key Innovations</h3>
            <div class="research-findings">
                <div class="finding-card">
                    <div class="finding-icon">🎯</div>
                    <h4>Budget Constraint Handling</h4>
                    <p>The algorithm explicitly handles fixed budget constraints, a critical requirement in real advertising scenarios.</p>
                </div>
                <div class="finding-card">
                    <div class="finding-icon">📈</div>
                    <h4>Adaptive Exploration</h4>
                    <p>Dynamically adjusts exploration based on campaign maturity and data availability.</p>
                </div>
                <div class="finding-card">
                    <div class="finding-icon">⚡</div>
                    <h4>Computational Efficiency</h4>
                    <p>Uses approximation techniques to make combinatorial optimization tractable for large-scale problems.</p>
                </div>
            </div>

            <h3>Performance Results</h3>
            <p>The study evaluated the algorithm on real advertising data with the following results:</p>
            <ul>
                <li><strong>15-30% improvement</strong> in cross-channel ROI compared to independent optimization</li>
                <li><strong>20-40% reduction</strong> in regret (difference from optimal) compared to standard MAB</li>
                <li><strong>Faster convergence</strong> to optimal allocation (50% fewer iterations needed)</li>
            </ul>

            <h2>Why This Matters: The Synergy Effect</h2>
            <p>One of the key insights from combinatorial bandit research is the <strong>synergy effect</strong>: certain combinations of campaigns perform better than the sum of their parts.</p>

            <div class="example-box">
                <h4>Example: Facebook + Google Synergy</h4>
                <p>Consider two campaigns:</p>
                <ul>
                    <li><strong>Facebook Campaign A:</strong> Standalone ROAS = 3.0x</li>
                    <li><strong>Google Campaign B:</strong> Standalone ROAS = 2.8x</li>
                </ul>
                <p>With independent optimization, you might allocate budget based on these individual ROAS values. But research shows that running both simultaneously can achieve:</p>
                <ul>
                    <li><strong>Combined ROAS = 3.5x</strong> (better than either alone)</li>
                    <li>Why? Cross-channel attribution, brand reinforcement, and complementary audience targeting</li>
                </ul>
                <p>Combinatorial bandits learn these synergies automatically.</p>
            </div>

            <h2>Implementation Challenges</h2>
            <p>While promising, combinatorial bandits face several practical challenges:</p>

            <h3>1. Computational Complexity</h3>
            <p>The number of possible combinations grows exponentially. With 10 campaigns, you have 2^10 = 1,024 combinations. With 20 campaigns, that's over 1 million.</p>
            <p><strong>Solution:</strong> Approximation algorithms and heuristics that focus on promising combinations.</p>

            <h3>2. Data Requirements</h3>
            <p>You need sufficient data for each combination to learn effectively. This can be challenging with many campaigns.</p>
            <p><strong>Solution:</strong> Transfer learning—using data from similar combinations to inform decisions.</p>

            <h3>3. Budget Constraints</h3>
            <p>Real-world budgets are fixed and must be allocated across all selected campaigns.</p>
            <p><strong>Solution:</strong> Constrained optimization techniques that respect budget limits.</p>

            <h2>Practical Applications</h2>
            <p>Combinatorial bandits are most valuable in these scenarios:</p>

            <div class="application-grid">
                <div class="app-card">
                    <h4>Cross-Platform Optimization</h4>
                    <p>Allocating budget across Facebook, Google, LinkedIn, and other platforms simultaneously.</p>
                </div>
                <div class="app-card">
                    <h4>Campaign Portfolio Management</h4>
                    <p>Selecting and optimizing combinations of campaigns within a single platform.</p>
                </div>
                <div class="app-card">
                    <h4>Creative Testing</h4>
                    <p>Testing combinations of creatives, audiences, and placements together.</p>
                </div>
                <div class="app-card">
                    <h4>Seasonal Campaign Coordination</h4>
                    <p>Coordinating multiple seasonal campaigns that interact with each other.</p>
                </div>
            </div>

            <h2>Comparison with Other Approaches</h2>
            <div class="comparison-table">
                <table>
                    <thead>
                        <tr>
                            <th>Approach</th>
                            <th>Pros</th>
                            <th>Cons</th>
                            <th>Best For</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Independent MAB</strong></td>
                            <td>Simple, fast</td>
                            <td>Ignores synergies</td>
                            <td>Single-channel optimization</td>
                        </tr>
                        <tr>
                            <td><strong>Greedy Allocation</strong></td>
                            <td>Very fast</td>
                            <td>Suboptimal, no learning</td>
                            <td>Static environments</td>
                        </tr>
                        <tr>
                            <td><strong>Combinatorial Bandits</strong></td>
                            <td>Learns synergies, optimal</td>
                            <td>Complex, data-intensive</td>
                            <td>Multichannel, large budgets</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <h2>Key Takeaways for Industry Leaders</h2>
            <div class="takeaways">
                <div class="takeaway-item">
                    <span class="takeaway-number">1</span>
                    <div>
                        <h4>Cross-channel synergies are real and valuable</h4>
                        <p>Research shows 15-30% improvement when optimizing combinations vs. independently.</p>
                    </div>
                </div>
                <div class="takeaway-item">
                    <span class="takeaway-number">2</span>
                    <div>
                        <h4>Combinatorial bandits are production-ready</h4>
                        <p>Recent research has made them computationally tractable for real-world use.</p>
                    </div>
                </div>
                <div class="takeaway-item">
                    <span class="takeaway-number">3</span>
                    <div>
                        <h4>Data quality is even more critical</h4>
                        <p>With more complex models, clean, accurate data becomes essential.</p>
                    </div>
                </div>
                <div class="takeaway-item">
                    <span class="takeaway-number">4</span>
                    <div>
                        <h4>Start simple, scale up</h4>
                        <p>Begin with 2-3 channels, then expand as you build confidence and data.</p>
                    </div>
                </div>
            </div>

            <h2>Research Papers & Further Reading</h2>
            <div class="research-papers">
                <div class="paper-card">
                    <h4>Adaptive Budget Optimization for Multichannel Advertising Using Combinatorial Bandits</h4>
                    <p class="paper-authors">B. Gangopadhyay, Z. Wang, A.S. Chiappa - arXiv preprint arXiv:2502.02920, 2025</p>
                    <p class="paper-abstract">Groundbreaking research on combinatorial bandits for multichannel advertising with budget constraints.</p>
                    <a href="https://arxiv.org/abs/2502.02920" target="_blank" class="paper-link">Read Paper →</a>
                </div>
                <div class="paper-card">
                    <h4>Multi-Armed Bandits Algorithms for Pricing and Advertising</h4>
                    <p class="paper-authors">M. Mussi - Springer, 2024-2025</p>
                    <p class="paper-abstract">Comprehensive overview of MAB algorithms including combinatorial variants.</p>
                    <a href="https://marcomussi.github.io/papers/springerbriefsphd/paper.pdf" target="_blank" class="paper-link">Read Paper →</a>
                </div>
            </div>

            <div class="cta-box">
                <h3>Ready to Optimize Across Multiple Channels?</h3>
                <p>Advera Labs uses combinatorial bandit algorithms to optimize your budget across Facebook, Google, and other platforms simultaneously. See the difference cross-channel optimization can make.</p>
                <a href="/#demo" class="btn-primary">Start Free Trial</a>
            </div>
            '''
        },
        9: {
            'title': 'Bayesian Multi-Armed Bandits: The Science Behind Smarter Ad Recommendations',
            'author': 'David Kim',
            'date': '2025-01-25',
            'category': 'Research',
            'read_time': '11 min read',
            'has_animations': True,
            'has_research_papers': True,
            'content': '''
            <div class="research-intro">
                <p class="lead">Bayesian approaches to multi-armed bandits represent one of the most elegant and effective frameworks for ad optimization. By combining prior knowledge with observed data, Bayesian bandits provide probabilistic reasoning that adapts naturally to uncertainty.</p>
                <p>This article explores how Bayesian multi-armed bandits work, why they're particularly well-suited for advertising, and what recent research tells us about their performance.</p>
            </div>

            <h2>The Bayesian Philosophy</h2>
            <p>Traditional frequentist statistics asks: "What's the probability of observing this data given a fixed parameter?" Bayesian statistics asks: "What's the probability distribution over possible parameters given this data?"</p>
            
            <p>In advertising terms:</p>
            <ul>
                <li><strong>Frequentist:</strong> "This campaign has a 3.2% conversion rate" (fixed, unknown)</li>
                <li><strong>Bayesian:</strong> "The conversion rate is likely between 2.8% and 3.6%, with 90% confidence" (probabilistic distribution)</li>
            </ul>

            <div class="animated-diagram">
                <div class="bayesian-visualization">
                    <div class="prior-distribution">
                        <h4>Prior Belief</h4>
                        <div class="distribution-bar" data-value="0.5" style="width: 50%"></div>
                        <p>Before seeing data, we have initial beliefs</p>
                    </div>
                    <div class="arrow">→</div>
                    <div class="data-observation">
                        <h4>Observe Data</h4>
                        <div class="data-points">
                            <span class="data-point success">✓</span>
                            <span class="data-point success">✓</span>
                            <span class="data-point fail">✗</span>
                            <span class="data-point success">✓</span>
                        </div>
                    </div>
                    <div class="arrow">→</div>
                    <div class="posterior-distribution">
                        <h4>Posterior Belief</h4>
                        <div class="distribution-bar" data-value="0.75" style="width: 75%"></div>
                        <p>Updated beliefs after seeing data</p>
                    </div>
                </div>
                <p class="diagram-caption">Bayesian updating: Start with prior beliefs, observe data, update to posterior beliefs. This happens continuously as new data arrives.</p>
            </div>

            <h2>How Bayesian Bandits Work</h2>
            <p>Bayesian multi-armed bandits maintain a probability distribution (usually Beta distribution for binary outcomes) over the reward rate of each arm.</p>

            <h3>Thompson Sampling: The Bayesian Bandit Algorithm</h3>
            <p>Thompson Sampling is the most popular Bayesian bandit algorithm. Here's how it works:</p>
            
            <div class="algorithm-steps">
                <div class="step-card">
                    <div class="step-number">1</div>
                    <div class="step-content">
                        <h4>Initialize Priors</h4>
                        <p>Start with prior distributions for each arm (often uniform, meaning no prior knowledge)</p>
                    </div>
                </div>
                <div class="step-card">
                    <div class="step-number">2</div>
                    <div class="step-content">
                        <h4>Sample from Distributions</h4>
                        <p>For each arm, sample a value from its current distribution</p>
                    </div>
                </div>
                <div class="step-card">
                    <div class="step-number">3</div>
                    <div class="step-content">
                        <h4>Select Best Sample</h4>
                        <p>Choose the arm with the highest sampled value</p>
                    </div>
                </div>
                <div class="step-card">
                    <div class="step-number">4</div>
                    <div class="step-content">
                        <h4>Observe Reward</h4>
                        <p>Play the selected arm and observe the outcome (conversion or not)</p>
                    </div>
                </div>
                <div class="step-card">
                    <div class="step-number">5</div>
                    <div class="step-content">
                        <h4>Update Distribution</h4>
                        <p>Update the arm's distribution using Bayesian updating</p>
                    </div>
                </div>
                <div class="step-card">
                    <div class="step-number">6</div>
                    <div class="step-content">
                        <h4>Repeat</h4>
                        <p>Go back to step 2 and continue</p>
                    </div>
                </div>
            </div>

            <h2>Why Bayesian Bandits Excel in Advertising</h2>
            <div class="research-findings">
                <div class="finding-card">
                    <div class="finding-icon">🎯</div>
                    <h4>Natural Uncertainty Handling</h4>
                    <p>Advertising is inherently uncertain. Bayesian methods quantify and work with this uncertainty rather than ignoring it.</p>
                </div>
                <div class="finding-card">
                    <div class="finding-icon">📊</div>
                    <h4>Prior Knowledge Integration</h4>
                    <p>You can incorporate domain knowledge (e.g., "this audience typically converts at 2-4%") as priors, accelerating learning.</p>
                </div>
                <div class="finding-card">
                    <div class="finding-icon">⚡</div>
                    <h4>Fast Convergence</h4>
                    <p>Research shows Bayesian bandits converge to optimal allocation faster than frequentist approaches, especially with good priors.</p>
                </div>
                <div class="finding-card">
                    <div class="finding-icon">🔄</div>
                    <h4>Adaptive Exploration</h4>
                    <p>Exploration naturally decreases as uncertainty decreases—no manual tuning needed.</p>
                </div>
            </div>

            <h2>Recent Research: Zeng (2025)</h2>
            <p>A 2025 study systematically evaluated Bayesian Multi-Armed Bandits in advertising recommendation scenarios through a 10,000-step simulation.</p>

            <h3>Key Findings</h3>
            <ul>
                <li><strong>Superior Performance:</strong> Bayesian MAB outperformed non-Bayesian approaches by 8-15% in cumulative reward</li>
                <li><strong>Faster Learning:</strong> Achieved optimal allocation 30-40% faster than UCB algorithms</li>
                <li><strong>Robust to Priors:</strong> Even with incorrect priors, performance degraded gracefully</li>
                <li><strong>Scalability:</strong> Maintained performance with up to 50 arms (campaigns)</li>
            </ul>

            <h2>Practical Implementation</h2>
            <h3>Choosing Priors</h3>
            <p>The choice of prior distribution matters, but less than you might think:</p>
            
            <div class="comparison-table">
                <table>
                    <thead>
                        <tr>
                            <th>Prior Type</th>
                            <th>Use Case</th>
                            <th>Impact</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Uniform (Beta(1,1))</strong></td>
                            <td>No prior knowledge</td>
                            <td>Neutral, learns from data</td>
                        </tr>
                        <tr>
                            <td><strong>Optimistic (Beta(2,1))</strong></td>
                            <td>Believe campaigns are good</td>
                            <td>Faster initial exploration</td>
                        </tr>
                        <tr>
                            <td><strong>Pessimistic (Beta(1,2))</strong></td>
                            <td>Conservative approach</td>
                            <td>More cautious exploration</td>
                        </tr>
                        <tr>
                            <td><strong>Informed (Beta(α,β))</strong></td>
                            <td>Historical data available</td>
                            <td>Accelerates learning significantly</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <h3>Handling Non-Binary Rewards</h3>
            <p>While Beta distributions work for binary outcomes (conversion/no conversion), real advertising often involves:</p>
            <ul>
                <li><strong>Revenue values:</strong> Use Normal-Gamma conjugate prior</li>
                <li><strong>Count data:</strong> Use Gamma-Poisson</li>
                <li><strong>Complex rewards:</strong> Use approximate Bayesian methods (variational inference, MCMC)</li>
            </ul>

            <h2>Comparison with Other Approaches</h2>
            <div class="comparison-table">
                <table>
                    <thead>
                        <tr>
                            <th>Algorithm</th>
                            <th>Uncertainty Handling</th>
                            <th>Prior Knowledge</th>
                            <th>Computational Cost</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Epsilon-Greedy</strong></td>
                            <td>None</td>
                            <td>No</td>
                            <td>Very Low</td>
                        </tr>
                        <tr>
                            <td><strong>UCB</strong></td>
                            <td>Confidence intervals</td>
                            <td>No</td>
                            <td>Low</td>
                        </tr>
                        <tr>
                            <td><strong>Thompson Sampling</strong></td>
                            <td>Full distributions</td>
                            <td>Yes</td>
                            <td>Medium</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <h2>Key Takeaways for Industry Leaders</h2>
            <div class="takeaways">
                <div class="takeaway-item">
                    <span class="takeaway-number">1</span>
                    <div>
                        <h4>Bayesian bandits are production-proven</h4>
                        <p>Used by major platforms (Google, Meta) and showing 8-15% improvement in research studies.</p>
                    </div>
                </div>
                <div class="takeaway-item">
                    <span class="takeaway-number">2</span>
                    <div>
                        <h4>Prior knowledge accelerates learning</h4>
                        <p>Even rough estimates of conversion rates can significantly improve performance.</p>
                    </div>
                </div>
                <div class="takeaway-item">
                    <span class="takeaway-number">3</span>
                    <div>
                        <h4>Uncertainty is a feature, not a bug</h4>
                        <p>Bayesian methods embrace uncertainty, leading to more robust decisions.</p>
                    </div>
                </div>
                <div class="takeaway-item">
                    <span class="takeaway-number">4</span>
                    <div>
                        <h4>Thompson Sampling is the go-to algorithm</h4>
                        <p>Simple to understand, easy to implement, excellent performance.</p>
                    </div>
                </div>
            </div>

            <h2>Research Papers & Further Reading</h2>
            <div class="research-papers">
                <div class="paper-card">
                    <h4>Optimizing Ad Recommendations Using A Bayesian Multi-Armed Bandit Approach</h4>
                    <p class="paper-authors">Y. Zeng - ITM Web of Conferences, 2025</p>
                    <p class="paper-abstract">Systematic evaluation of Bayesian MAB in advertising through 10,000-step simulation.</p>
                    <a href="https://www.itm-conferences.org/articles/itmconf/abs/2025/09/itmconf_cseit2025_04026/itmconf_cseit2025_04026.html" target="_blank" class="paper-link">Read Paper →</a>
                </div>
                <div class="paper-card">
                    <h4>A Bayesian Multi-Armed Bandit Algorithm for Bid Shading in Online Display Advertising</h4>
                    <p class="paper-authors">M. Guo, W. Zhang, C. Yuan, B. Jia, G. Song - ACM CIKM, 2024</p>
                    <p class="paper-abstract">Application of Bayesian bandits to bid shading in programmatic advertising.</p>
                    <a href="https://dl.acm.org/doi/abs/10.1145/3627673.3680107" target="_blank" class="paper-link">Read Paper →</a>
                </div>
            </div>

            <div class="cta-box">
                <h3>Ready to Leverage Bayesian Optimization?</h3>
                <p>Advera Labs uses Bayesian multi-armed bandit algorithms to make smarter ad optimization decisions. Experience the power of probabilistic reasoning.</p>
                <a href="/#demo" class="btn-primary">Start Free Trial</a>
            </div>
            '''
        },
        10: {
            'title': 'Reinforcement Learning Meets Advertising: A Practical Guide to RL-Based Optimization',
            'author': 'Dr. Emily Rodriguez',
            'date': '2025-01-22',
            'category': 'Research',
            'read_time': '14 min read',
            'has_animations': True,
            'has_research_papers': True,
            'content': '''
            <div class="research-intro">
                <p class="lead">Reinforcement Learning (RL) represents the cutting edge of ad optimization. While multi-armed bandits focus on immediate rewards, RL algorithms can learn complex, long-term strategies that adapt to changing environments.</p>
                <p>This article explores how RL is revolutionizing ad optimization, from simple Q-learning to sophisticated actor-critic methods, and what recent research tells us about their real-world performance.</p>
            </div>

            <h2>From Bandits to Reinforcement Learning</h2>
            <p>Multi-armed bandits are actually a special case of reinforcement learning—they're RL with a single state. Full RL adds:</p>
            <ul>
                <li><strong>State representation:</strong> Context about the environment (user, time, season, etc.)</li>
                <li><strong>Action sequences:</strong> Learning sequences of actions, not just single decisions</li>
                <li><strong>Long-term rewards:</strong> Optimizing for cumulative reward over time, not just immediate</li>
            </ul>

            <div class="animated-diagram">
                <div class="rl-visualization">
                    <div class="rl-cycle">
                        <div class="rl-state">
                            <h4>State</h4>
                            <p>User context, campaign performance, time of day</p>
                        </div>
                        <div class="arrow">→</div>
                        <div class="rl-action">
                            <h4>Action</h4>
                            <p>Allocate budget, adjust bid, pause campaign</p>
                        </div>
                        <div class="arrow">→</div>
                        <div class="rl-reward">
                            <h4>Reward</h4>
                            <p>Conversion, revenue, profit</p>
                        </div>
                        <div class="arrow">→</div>
                        <div class="rl-next-state">
                            <h4>Next State</h4>
                            <p>Updated context after action</p>
                        </div>
                    </div>
                </div>
                <p class="diagram-caption">RL cycle: Agent observes state, takes action, receives reward, transitions to next state. The agent learns a policy (strategy) that maximizes long-term cumulative reward.</p>
            </div>

            <h2>Key RL Algorithms for Advertising</h2>
            
            <h3>1. Q-Learning</h3>
            <p>Q-learning learns the value (Q-value) of taking an action in a given state. Simple and effective for discrete state/action spaces.</p>
            <div class="algorithm-box">
                <strong>Best for:</strong> Simple optimization problems with discrete states (e.g., budget tiers, campaign on/off)<br>
                <strong>Limitation:</strong> Doesn't scale well to continuous or high-dimensional spaces
            </div>

            <h3>2. Deep Q-Networks (DQN)</h3>
            <p>Uses neural networks to approximate Q-values, enabling RL in complex, high-dimensional state spaces.</p>
            <div class="algorithm-box">
                <strong>Best for:</strong> Complex state representations (user features, campaign history, contextual data)<br>
                <strong>Advantage:</strong> Can handle thousands of features simultaneously
            </div>

            <h3>3. Policy Gradient Methods</h3>
            <p>Directly learn the policy (action selection strategy) rather than value functions. Includes REINFORCE, Actor-Critic, PPO.</p>
            <div class="algorithm-box">
                <strong>Best for:</strong> Continuous action spaces (e.g., bid amounts, budget percentages)<br>
                <strong>Advantage:</strong> More stable learning, better for continuous control
            </div>

            <h3>4. Actor-Critic Methods</h3>
            <p>Combine policy learning (actor) with value estimation (critic) for more stable and efficient learning.</p>
            <div class="algorithm-box">
                <strong>Best for:</strong> Complex advertising scenarios requiring both exploration and exploitation<br>
                <strong>Advantage:</strong> State-of-the-art performance, used in production systems
            </div>

            <h2>Recent Research: Sathvika & Pradeep (2025)</h2>
            <p>A 2025 study explored the use of Multi-Armed Bandit framework combined with reinforcement learning for advertisement optimization.</p>

            <h3>Key Findings</h3>
            <div class="research-findings">
                <div class="finding-card">
                    <div class="finding-icon">📊</div>
                    <h4>Superior Long-Term Performance</h4>
                    <p>RL-based approaches showed 20-30% improvement in cumulative reward over 30-day periods compared to myopic optimization.</p>
                </div>
                <div class="finding-card">
                    <div class="finding-icon">🔄</div>
                    <h4>Adaptation to Changes</h4>
                    <p>RL algorithms adapted 3x faster to seasonal changes and market shifts compared to static optimization.</p>
                </div>
                <div class="finding-card">
                    <div class="finding-icon">🎯</div>
                    <h4>Complex Strategy Learning</h4>
                    <p>Learned sophisticated strategies like "increase budget on weekends" and "shift to mobile during commute hours" automatically.</p>
                </div>
            </div>

            <h2>State Representation in Advertising</h2>
            <p>The state in RL represents everything the agent needs to know to make decisions. For advertising, this includes:</p>

            <div class="state-components">
                <div class="state-group">
                    <h4>User Context</h4>
                    <ul>
                        <li>Demographics</li>
                        <li>Past behavior</li>
                        <li>Device, location</li>
                        <li>Time of day, day of week</li>
                    </ul>
                </div>
                <div class="state-group">
                    <h4>Campaign State</h4>
                    <ul>
                        <li>Current performance (ROAS, CPA)</li>
                        <li>Budget remaining</li>
                        <li>Campaign age/maturity</li>
                        <li>Competitive landscape</li>
                    </ul>
                </div>
                <div class="state-group">
                    <h4>Market Context</h4>
                    <ul>
                        <li>Seasonality</li>
                        <li>Competitor activity</li>
                        <li>Economic indicators</li>
                        <li>Platform changes</li>
                    </ul>
                </div>
            </div>

            <h2>Actions in RL-Based Ad Optimization</h2>
            <p>RL agents can learn to take various actions:</p>
            <ul>
                <li><strong>Budget allocation:</strong> How much to spend on each campaign</li>
                <li><strong>Bid adjustment:</strong> Increase/decrease bids based on context</li>
                <li><strong>Campaign management:</strong> Pause, scale, or modify campaigns</li>
                <li><strong>Creative selection:</strong> Which ad creative to show</li>
                <li><strong>Audience targeting:</strong> Adjust targeting parameters</li>
            </ul>

            <h2>Reward Design: Critical for Success</h2>
            <p>How you define reward determines what the agent optimizes for. Common approaches:</p>

            <div class="comparison-table">
                <table>
                    <thead>
                        <tr>
                            <th>Reward Function</th>
                            <th>What It Optimizes</th>
                            <th>Pros</th>
                            <th>Cons</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Immediate Revenue</strong></td>
                            <td>Short-term revenue</td>
                            <td>Simple, direct</td>
                            <td>Ignores long-term value</td>
                        </tr>
                        <tr>
                            <td><strong>Cumulative ROAS</strong></td>
                            <td>Efficiency over time</td>
                            <td>Balances spend and return</td>
                            <td>May miss profit opportunities</td>
                        </tr>
                        <tr>
                            <td><strong>Profit (Revenue - Cost)</strong></td>
                            <td>Actual profit</td>
                            <td>Business-aligned</td>
                            <td>Requires margin data</td>
                        </tr>
                        <tr>
                            <td><strong>LTV-Adjusted</strong></td>
                            <td>Customer lifetime value</td>
                            <td>Long-term focus</td>
                            <td>Complex, delayed feedback</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <h2>Challenges and Solutions</h2>
            
            <h3>1. Delayed Feedback</h3>
            <p><strong>Problem:</strong> Conversions may happen days or weeks after ad exposure.</p>
            <p><strong>Solution:</strong> Use reward shaping, attribution models, or delayed reward RL algorithms.</p>

            <h3>2. Non-Stationarity</h3>
            <p><strong>Problem:</strong> Advertising environments change constantly (seasonality, competition, platform updates).</p>
            <p><strong>Solution:</strong> Use online learning, forgetting mechanisms, or meta-learning approaches.</p>

            <h3>3. Exploration vs. Exploitation</h3>
            <p><strong>Problem:</strong> Need to explore new strategies while exploiting what works.</p>
            <p><strong>Solution:</strong> Epsilon-greedy, UCB, or Thompson sampling for action selection.</p>

            <h3>4. Sample Efficiency</h3>
            <p><strong>Problem:</strong> RL typically requires many samples to learn.</p>
            <p><strong>Solution:</strong> Transfer learning, imitation learning, or hybrid approaches combining RL with supervised learning.</p>

            <h2>Real-World Applications</h2>
            <div class="application-grid">
                <div class="app-card">
                    <h4>Dynamic Bidding</h4>
                    <p>RL agents learn optimal bid amounts based on user context, competition, and campaign goals.</p>
                </div>
                <div class="app-card">
                    <h4>Budget Reallocation</h4>
                    <p>Continuously shift budgets between campaigns based on learned performance patterns.</p>
                </div>
                <div class="app-card">
                    <h4>Creative Optimization</h4>
                    <p>Learn which creatives work best for which audiences and contexts.</p>
                </div>
                <div class="app-card">
                    <h4>Cross-Channel Coordination</h4>
                    <p>Coordinate strategies across multiple platforms simultaneously.</p>
                </div>
            </div>

            <h2>Key Takeaways for Industry Leaders</h2>
            <div class="takeaways">
                <div class="takeaway-item">
                    <span class="takeaway-number">1</span>
                    <div>
                        <h4>RL enables long-term strategic thinking</h4>
                        <p>Unlike bandits, RL can learn complex, multi-step strategies that adapt to changing conditions.</p>
                    </div>
                </div>
                <div class="takeaway-item">
                    <span class="takeaway-number">2</span>
                    <div>
                        <h4>State representation is critical</h4>
                        <p>What you include in the state determines what the agent can learn. More context = better decisions.</p>
                    </div>
                </div>
                <div class="takeaway-item">
                    <span class="takeaway-number">3</span>
                    <div>
                        <h4>Reward design drives behavior</h4>
                        <p>Carefully design rewards to align with business goals. Profit-based rewards lead to profit optimization.</p>
                    </div>
                </div>
                <div class="takeaway-item">
                    <span class="takeaway-number">4</span>
                    <div>
                        <h4>Start simple, scale up</h4>
                        <p>Begin with simple Q-learning or bandits, then add complexity as you gain experience and data.</p>
                    </div>
                </div>
            </div>

            <h2>Research Papers & Further Reading</h2>
            <div class="research-papers">
                <div class="paper-card">
                    <h4>Reinforcement Learning for Optimizing Advertisement Selection in Digital Marketing: A Study of Multi-Armed Bandit Algorithms</h4>
                    <p class="paper-authors">P. Sathvika, D.J. Pradeep - 2025 17th International Conference, IEEE</p>
                    <p class="paper-abstract">Comprehensive study of RL-based MAB for advertisement optimization.</p>
                    <a href="https://ieeexplore.ieee.org/abstract/document/11338484/" target="_blank" class="paper-link">Read Paper →</a>
                </div>
                <div class="paper-card">
                    <h4>Utilizing reinforcement learning bandit algorithms in advertising optimization</h4>
                    <p class="paper-authors">S. Zhang - Highlights in Science, Engineering and Technology, 2024</p>
                    <p class="paper-abstract">Explores RL-based approaches to bandit problems in advertising.</p>
                    <a href="https://pdfs.semanticscholar.org/14b1/b97f36bb01333e6863a60c781373f6cba906.pdf" target="_blank" class="paper-link">Read Paper →</a>
                </div>
            </div>

            <div class="cta-box">
                <h3>Ready to Leverage Reinforcement Learning?</h3>
                <p>Advera Labs uses advanced RL algorithms to learn complex optimization strategies automatically. Experience the future of ad optimization.</p>
                <a href="/#demo" class="btn-primary">Start Free Trial</a>
            </div>
            '''
        },
        1: {
            'title': 'Why LTV-Based Optimization Beats ROAS Every Time',
            'author': 'Sarah Chen',
            'date': '2025-01-15',
            'category': 'Optimization',
            'read_time': '5 min read',
            'content': '''
            <p>Most advertisers optimize for ROAS (Return on Ad Spend), but smart marketers know that ROAS alone doesn't tell the full story. Here's why LTV-based optimization delivers better business outcomes.</p>
            
            <h2>The ROAS Problem</h2>
            <p>ROAS measures revenue per dollar spent, but it ignores critical business factors:</p>
            <ul>
                <li><strong>Profit margins:</strong> A 4x ROAS campaign might have 20% margins, while a 3x ROAS campaign has 40% margins—the latter is more profitable</li>
                <li><strong>Customer lifetime value:</strong> A customer who buys once vs. one who subscribes for 12 months have vastly different LTVs</li>
                <li><strong>Acquisition costs:</strong> ROAS doesn't account for the true cost of acquiring a customer</li>
            </ul>
            
            <h2>Why LTV Optimization Wins</h2>
            <p>When you optimize for LTV, you're making decisions based on the true value of each customer:</p>
            <ul>
                <li>Prioritize high-LTV customer segments</li>
                <li>Allocate budget to campaigns that attract repeat buyers</li>
                <li>Focus on profitable growth, not just revenue</li>
            </ul>
            
            <h2>Real Results</h2>
            <p>Brands using LTV-based optimization see:</p>
            <ul>
                <li>20-30% improvement in profit margins</li>
                <li>Better customer retention rates</li>
                <li>More sustainable growth</li>
            </ul>
            
            <p>Ready to optimize for profit instead of just revenue? <a href="/#demo">Start your free trial</a> today.</p>
            '''
        },
        2: {
            'title': 'The Hidden Cost of Misconfigured Conversion Tracking',
            'author': 'Michael Park',
            'date': '2025-01-10',
            'category': 'Tracking',
            'read_time': '7 min read',
            'content': '''
            <p>Your Smart Bidding campaigns are only as good as the signals you feed them. Misconfigured conversion tracking is silently costing you 10-20% of your ad budget.</p>
            
            <h2>Common Tracking Issues</h2>
            <p>We've audited hundreds of ad accounts and found these recurring problems:</p>
            <ul>
                <li><strong>Wrong primary conversion:</strong> Optimizing for "add to cart" instead of "purchase"</li>
                <li><strong>Missing conversion values:</strong> Platforms can't optimize for revenue without value data</li>
                <li><strong>Broken pixels:</strong> Server-side tracking not set up, missing events</li>
                <li><strong>Low conversion volume:</strong> Not enough data for Smart Bidding to work effectively</li>
            </ul>
            
            <h2>The Impact</h2>
            <p>When tracking is broken, Smart Bidding algorithms:</p>
            <ul>
                <li>Optimize for the wrong events</li>
                <li>Can't distinguish high-value from low-value conversions</li>
                <li>Waste budget on low-quality traffic</li>
            </ul>
            
            <h2>How to Fix It</h2>
            <p>Our ROI Audit feature automatically detects these issues and provides actionable recommendations. Most brands recover 10-20% of wasted spend just by fixing tracking.</p>
            
            <p><a href="/#demo">Run a free ROI audit</a> to see what's costing you money.</p>
            '''
        },
        # Add more posts as needed
    }
    
    post = posts_data.get(post_id)
    if not post:
        from django.http import Http404
        raise Http404("Blog post not found")
    
    context = {
        'page_title': f"{post['title']} - Advera Labs Blog",
        'post': post,
    }
    return render(request, 'website/blog_post.html', context)


def careers(request):
    """Careers page view."""
    job_openings = [
        {
            'id': 1,
            'title': 'Senior Backend Engineer',
            'department': 'Engineering',
            'location': 'Remote / San Francisco',
            'type': 'Full-time',
            'description': 'Build the core optimization engine that powers our AI-driven budget allocation system.',
            'requirements': [
                '5+ years Python experience',
                'Experience with ML/optimization algorithms',
                'Strong background in distributed systems',
                'Knowledge of ad tech APIs (Meta, Google Ads)'
            ]
        },
        {
            'id': 2,
            'title': 'Product Marketing Manager',
            'department': 'Marketing',
            'location': 'Remote / New York',
            'type': 'Full-time',
            'description': 'Lead product marketing for our B2B SaaS platform, targeting performance marketers and agencies.',
            'requirements': [
                '3+ years B2B SaaS marketing experience',
                'Strong understanding of ad tech/martech',
                'Experience with PLG (Product-Led Growth)',
                'Excellent writing and communication skills'
            ]
        },
        {
            'id': 3,
            'title': 'Customer Success Manager',
            'department': 'Customer Success',
            'location': 'Remote',
            'type': 'Full-time',
            'description': 'Help customers maximize value from Advera Labs, ensuring they achieve ROI targets and grow their accounts.',
            'requirements': [
                '2+ years in customer success or account management',
                'Experience with performance marketing tools',
                'Strong analytical and problem-solving skills',
                'Excellent relationship-building abilities'
            ]
        },
        {
            'id': 4,
            'title': 'Data Scientist',
            'department': 'Engineering',
            'location': 'Remote / Seattle',
            'type': 'Full-time',
            'description': 'Develop ML models for LTV prediction, incrementality measurement, and budget optimization.',
            'requirements': [
                '3+ years in data science/ML',
                'Experience with time series, causal inference',
                'Strong Python and SQL skills',
                'Background in ad tech or e-commerce preferred'
            ]
        },
    ]
    
    context = {
        'page_title': 'Careers - Advera Labs',
        'job_openings': job_openings,
    }
    return render(request, 'website/careers.html', context)


def contact(request):
    """Contact page view."""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        company = request.POST.get('company')
        message = request.POST.get('message')
        subject = request.POST.get('subject', 'General Inquiry')
        
        # In production, you'd send an email or save to database
        # For now, just show success message
        messages.success(request, 'Thank you for contacting us! We\'ll get back to you within 24 hours.')
        
        # Redirect to avoid resubmission
        from django.shortcuts import redirect
        return redirect('contact')
    
    context = {
        'page_title': 'Contact Us - Advera Labs',
    }
    return render(request, 'website/contact.html', context)


def documentation(request):
    """Documentation page view."""
    context = {
        'page_title': 'Documentation - Advera Labs',
    }
    return render(request, 'website/documentation.html', context)


def api_docs(request):
    """API documentation page view."""
    context = {
        'page_title': 'API Documentation - Advera Labs',
    }
    return render(request, 'website/api.html', context)


def support(request):
    """Support page view."""
    context = {
        'page_title': 'Support - Advera Labs',
    }
    return render(request, 'website/support.html', context)


def privacy(request):
    """Privacy Policy page view."""
    context = {
        'page_title': 'Privacy Policy - Advera Labs',
    }
    return render(request, 'website/privacy.html', context)
