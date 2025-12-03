import gradio as gr

# variables to track game state
low = 1
high = 100
guess = 50
steps = 1
active = True

def new_game():
    """Reset everything for a new game"""
    global low, high, guess, steps, active
    low = 1
    high = 100
    guess = (low + high) // 2  # Start in the middle
    steps = 1
    active = True
    return update_display()

def update_display():
    """Update all the display components"""
    
    # Create the main guess box
    if active:
        guess_box = f"""
<div style="text-align: center; padding: 40px 30px; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
     border-radius: 20px; margin: 20px 0; box-shadow: 0 20px 40px rgba(0,0,0,0.4);">
    <div style="color: rgba(255,255,255,0.9); font-size: 12px; margin-bottom: 10px; font-weight: 600; 
         text-transform: uppercase; letter-spacing: 2px;">My Guess</div>
    <div style="color: white; font-size: 72px; font-weight: bold;">{guess}</div>
    <div style="display: flex; justify-content: center; gap: 15px; margin-top: 20px; color: white; font-size: 12px;">
        <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 8px;">
            Step {steps}
        </span>
        <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 8px;">
            Range: {low}-{high}
        </span>
        <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 8px;">
            {high-low+1} left
        </span>
    </div>
</div>
        """
    else:
        # Show success message when found
        guess_box = f"""
<div style="text-align: center; padding: 50px 30px; background: linear-gradient(135deg, #10b981 0%, #059669 100%);
     border-radius: 20px; margin: 20px 0; box-shadow: 0 20px 40px rgba(16,185,129,0.4);">
    <div style="font-size: 40px; margin-bottom: 15px;">🎉</div>
    <div style="color: white; font-size: 28px; margin-bottom: 15px; font-weight: bold; text-transform: uppercase;">
        Found It!
    </div>
    <div style="color: white; font-size: 72px; font-weight: bold; margin: 15px 0;">{guess}</div>
    <div style="color: white; font-size: 16px; margin-top: 15px;">
        Solved in {steps} step{"s" if steps != 1 else ""}
    </div>
</div>
        """
    
    # Generate the number grid
    grid = create_grid()
    
    # Create stats panel
    if active:
        stats = f"""
<div style="background: rgba(30,41,59,0.8); padding: 25px; border-radius: 20px; 
     border: 1px solid rgba(255,255,255,0.1); margin-top: 20px;">
    <div style="font-size: 18px; color: #f1f5f9; margin-bottom: 15px; font-weight: bold;">
        📊 Stats
    </div>
    <div style="color: #cbd5e1; font-size: 13px; line-height: 2;">
        <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
            <span style="color: #94a3b8;">Steps</span>
            <span style="color: white; font-weight: bold;">{steps}</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
            <span style="color: #94a3b8;">Range</span>
            <span style="color: white; font-weight: bold;">{low} → {high}</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 10px 0;">
            <span style="color: #94a3b8;">Time Complexity</span>
            <span style="color: #10b981; font-weight: bold;">O(log n)</span>
        </div>
    </div>
</div>
        """
    else:
        # Calculate how well they did
        if steps <= 7:
            efficiency = ((8-steps)/7*100)
        else:
            efficiency = 50
            
        stats = f"""
<div style="background: linear-gradient(135deg, rgba(16,185,129,0.2) 0%, rgba(5,150,105,0.2) 100%); 
     padding: 30px; border-radius: 20px; margin-top: 20px; border: 1px solid rgba(16,185,129,0.3);">
    <div style="font-size: 22px; color: #10b981; margin-bottom: 15px; font-weight: bold; text-align: center;">
        ✓ Complete!
    </div>
    <div style="color: #d1fae5; font-size: 14px; line-height: 1.8;">
        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
            <span>Your Number</span>
            <span style="font-weight: bold; color: white;">{guess}</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
            <span>Steps</span>
            <span style="font-weight: bold; color: white;">{steps}</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
            <span>Max Steps</span>
            <span style="font-weight: bold; color: white;">7</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 8px 0;">
            <span>Efficiency</span>
            <span style="font-weight: bold; color: white;">{efficiency:.0f}%</span>
        </div>
    </div>
    
    <div style="margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 12px; text-align: center;">
        <div style="color: white; font-size: 16px; font-weight: bold;">
            {get_rating(steps)}
        </div>
    </div>
</div>
        """
    
    return guess_box, grid, stats

def get_rating(steps):
    """Return a rating based on number of steps"""
    if steps == 1:
        return "🏆 Perfect!"
    elif steps <= 3:
        return "⭐ Excellent!"
    elif steps <= 5:
        return "✨ Great!"
    elif steps <= 7:
        return "👍 Good!"
    else:
        return "✓ Done!"

def create_grid():
    """Create the 10x10 number grid"""
    html = """
<div style="background: rgba(30,41,59,0.6); padding: 35px; border-radius: 20px; 
     box-shadow: 0 10px 40px rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.1);">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
        <div style="font-size: 20px; color: #f1f5f9; font-weight: bold;">
            🔢 Numbers 1-100
        </div>
        <div style="display: flex; gap: 20px; font-size: 13px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 16px; height: 16px; background: linear-gradient(135deg, #6366f1, #8b5cf6); 
                     border-radius: 4px;"></div>
                <span style="color: #cbd5e1;">Current</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 16px; height: 16px; background: #10b981; border-radius: 4px;"></div>
                <span style="color: #cbd5e1;">Found</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 16px; height: 16px; background: rgba(71,85,105,0.4); border-radius: 4px;"></div>
                <span style="color: #cbd5e1;">Eliminated</span>
            </div>
        </div>
    </div>
    <div style="display: grid; grid-template-columns: repeat(10, 1fr); gap: 8px; font-size: 16px;">
"""
    
    # Loop through all 100 numbers
    for i in range(1, 101):
        eliminated = (i < low or i > high)
        current = (i == guess)
        
        if current and active:
            # This is the current guess - make it purple
            html += f'''<div style="background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; 
                padding: 14px; border-radius: 10px; font-weight: bold; text-align: center; 
                box-shadow: 0 4px 15px rgba(99,102,241,0.6); transform: scale(1.05);">{i}</div>'''
        elif current and not active:
            # Found it! Make it green
            html += f'''<div style="background: linear-gradient(135deg, #10b981, #059669); color: white; 
                padding: 14px; border-radius: 10px; font-weight: bold; text-align: center; 
                box-shadow: 0 4px 20px rgba(16,185,129,0.8); transform: scale(1.1);">🎯{i}</div>'''
        elif eliminated or not active:
            # Eliminated - gray it out
            html += f'''<div style="background: rgba(71,85,105,0.3); color: #64748b; padding: 14px; 
                border-radius: 10px; text-align: center; opacity: 0.4; text-decoration: line-through;">{i}</div>'''
        elif active:
            # Still in play
            html += f'''<div style="background: rgba(51,65,85,0.6); color: #e2e8f0; padding: 14px; 
                border-radius: 10px; font-weight: 600; text-align: center; 
                border: 1px solid rgba(148,163,184,0.2);">{i}</div>'''
        else:
            html += f'<div style="padding: 14px; text-align: center; color: #64748b;">{i}</div>'
    
    html += """
    </div>
</div>
"""
    return html

def higher():
    """User says their number is higher than the guess"""
    global low, guess, steps, active
    
    if not active:
        return update_display()
    
    low = guess + 1  # Eliminate everything below
    
    if low > high:
        active = False
        return update_display()
    
    guess = (low + high) // 2  # New guess is middle of remaining range
    steps += 1
    
    return update_display()

def lower():
    """User says their number is lower than the guess"""
    global high, guess, steps, active
    
    if not active:
        return update_display()
    
    high = guess - 1  # Eliminate everything above
    
    if low > high:
        active = False
        return update_display()
    
    guess = (low + high) // 2  # New guess is middle of remaining range
    steps += 1
    
    return update_display()

def correct():
    """User says we guessed correctly"""
    global active
    
    if not active:
        return update_display()
    
    active = False
    return update_display()

# Create the Gradio interface
with gr.Blocks(title="Binary Search Game") as app:
    
    # Header
    with gr.Row():
        with gr.Column():
            gr.HTML("""
                <div style="text-align: center; padding: 50px 20px 30px 20px; 
                     background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);">
                    <div style="display: inline-block; padding: 8px 20px; background: rgba(99,102,241,0.15); 
                         border-radius: 20px; margin-bottom: 20px; border: 1px solid rgba(99,102,241,0.3);">
                        <span style="color: #a5b4fc; font-size: 13px; font-weight: 600; text-transform: uppercase;">
                            Algorithm Visualizer
                        </span>
                    </div>
                    <h1 style="font-size: 56px; font-weight: bold; color: #f1f5f9; margin-bottom: 15px;">
                        Binary Search Game
                    </h1>
                    <p style="font-size: 18px; color: #94a3b8; max-width: 600px; margin: 0 auto;">
                        Think of a number from 1 to 100 and I'll find it in 7 steps or less!
                    </p>
                </div>
            """)
    
    gr.HTML("<div style='border-top: 1px solid rgba(255,255,255,0.1); margin: 20px 0;'></div>")
    
    # Main content
    with gr.Row():
        with gr.Column(scale=7):
            grid_display = gr.HTML(create_grid())
        
        with gr.Column(scale=3):
            # Guess display
            guess_display = gr.HTML("""
<div style="text-align: center; padding: 40px 30px; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
     border-radius: 20px; margin: 20px 0; box-shadow: 0 20px 40px rgba(0,0,0,0.4);">
    <div style="color: rgba(255,255,255,0.9); font-size: 12px; margin-bottom: 10px; font-weight: 600; 
         text-transform: uppercase; letter-spacing: 2px;">My Guess</div>
    <div style="color: white; font-size: 72px; font-weight: bold;">50</div>
    <div style="display: flex; justify-content: center; gap: 15px; margin-top: 20px; color: white; font-size: 12px;">
        <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 8px;">Step 1</span>
        <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 8px;">Range: 1-100</span>
        <span style="background: rgba(255,255,255,0.2); padding: 6px 12px; border-radius: 8px;">100 left</span>
    </div>
</div>
            """)
            
            gr.HTML("""<div style='margin: 15px 0; text-align: center;'>
                <div style='color: #94a3b8; font-weight: bold; font-size: 12px; text-transform: uppercase;'>
                    Is your number...
                </div>
            </div>""")
            
            # Buttons
            up_btn = gr.Button("⬆️  Higher", size="lg", variant="primary")
            ok_btn = gr.Button("✓  Correct", size="lg", variant="stop")
            dn_btn = gr.Button("⬇️  Lower", size="lg", variant="primary")
            
            gr.HTML("<div style='margin: 20px 0;'></div>")
            
            new_btn = gr.Button("🔄 New Game", size="lg", variant="secondary")
            
            # Stats display
            status_display = gr.HTML("""
<div style="background: rgba(30,41,59,0.8); padding: 25px; border-radius: 20px; 
     border: 1px solid rgba(255,255,255,0.1); margin-top: 20px;">
    <div style="font-size: 18px; color: #f1f5f9; margin-bottom: 15px; font-weight: bold;">📊 Stats</div>
    <div style="color: #cbd5e1; font-size: 13px; line-height: 2;">
        <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
            <span style="color: #94a3b8;">Steps</span>
            <span style="color: white; font-weight: bold;">1</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
            <span style="color: #94a3b8;">Range</span>
            <span style="color: white; font-weight: bold;">1 → 100</span>
        </div>
        <div style="display: flex; justify-content: space-between; padding: 10px 0;">
            <span style="color: #94a3b8;">Time Complexity</span>
            <span style="color: #10b981; font-weight: bold;">O(log n)</span>
        </div>
    </div>
</div>
            """)
    
    gr.HTML("<div style='border-top: 1px solid rgba(255,255,255,0.1); margin: 40px 0;'></div>")
    
    # How it works section
    with gr.Accordion("📚 How Binary Search Works", open=False):
        gr.HTML("""
<div style="padding: 30px; color: #cbd5e1; background: rgba(30,41,59,0.5); border-radius: 16px;">
    <h3 style="color: #f1f5f9; margin-bottom: 20px; font-weight: bold; font-size: 24px;">
        About Binary Search
    </h3>
    
    <p style="font-size: 16px; margin-bottom: 25px;">
        Binary search is a super efficient algorithm for finding things in sorted lists. 
        Instead of checking every number one by one, it eliminates half the possibilities with each guess!
    </p>
    
    <div style="background: rgba(99,102,241,0.1); padding: 25px; border-radius: 12px; margin: 25px 0; 
         border-left: 4px solid #6366f1;">
        <h4 style="color: #c7d2fe; margin-bottom: 15px; font-weight: bold;">The Algorithm</h4>
        <ol style="margin: 0; padding-left: 25px; font-size: 15px; line-height: 2;">
            <li>Start by guessing the middle number (50)</li>
            <li>If too high, eliminate all numbers above</li>
            <li>If too low, eliminate all numbers below</li>
            <li>Keep cutting the remaining numbers in half until you find it!</li>
        </ol>
    </div>
    
    <h4 style="color: #f1f5f9; margin: 30px 0 15px 0; font-weight: bold;">Why It's Fast</h4>
    <div style="background: rgba(51,65,85,0.3); padding: 20px; border-radius: 12px; margin: 20px 0;">
        <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
            <tr style="border-bottom: 2px solid rgba(148,163,184,0.2);">
                <th style="padding: 12px; text-align: left; color: #cbd5e1;">Numbers</th>
                <th style="padding: 12px; text-align: center; color: #cbd5e1;">Linear Search</th>
                <th style="padding: 12px; text-align: center; color: #cbd5e1;">Binary Search</th>
            </tr>
            <tr style="border-bottom: 1px solid rgba(148,163,184,0.1);">
                <td style="padding: 12px; color: #e2e8f0;">1-100</td>
                <td style="padding: 12px; text-align: center; color: #f87171;">up to 100</td>
                <td style="padding: 12px; text-align: center; color: #10b981; font-weight: bold;">max 7</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(148,163,184,0.1);">
                <td style="padding: 12px; color: #e2e8f0;">1-1,000</td>
                <td style="padding: 12px; text-align: center; color: #f87171;">up to 1,000</td>
                <td style="padding: 12px; text-align: center; color: #10b981; font-weight: bold;">max 10</td>
            </tr>
            <tr>
                <td style="padding: 12px; color: #e2e8f0;">1-1,000,000</td>
                <td style="padding: 12px; text-align: center; color: #f87171;">up to 1,000,000</td>
                <td style="padding: 12px; text-align: center; color: #10b981; font-weight: bold;">max 20</td>
            </tr>
        </table>
    </div>
    
    <div style="margin-top: 30px; padding: 25px; background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.15)); 
         border-radius: 12px; border: 1px solid rgba(99,102,241,0.3);">
        <div style="display: flex; gap: 15px;">
            <div style="font-size: 32px;">💡</div>
            <div>
                <div style="color: #c7d2fe; font-weight: bold; font-size: 16px; margin-bottom: 8px;">
                    Key Takeaway
                </div>
                <div style="color: #cbd5e1; font-size: 14px; line-height: 1.7;">
                    By cutting the search space in half each time, binary search can find any number in a list of 
                    1 million items in just 20 guesses! That's the power of O(log n) time complexity.
                </div>
            </div>
        </div>
    </div>
</div>
        """)
    
    # Connect the buttons to functions
    new_btn.click(new_game, outputs=[guess_display, grid_display, status_display])
    up_btn.click(higher, outputs=[guess_display, grid_display, status_display])
    dn_btn.click(lower, outputs=[guess_display, grid_display, status_display])
    ok_btn.click(correct, outputs=[guess_display, grid_display, status_display])

# Run the app
if __name__ == "__main__":
    app.launch()
