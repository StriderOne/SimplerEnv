import plotly.graph_objects as go
import numpy as np
import plotly.offline as pyo
import plotly.io as pio

from simpler_env.utils.metrics import mean_maximum_rank_violation, pearson_correlation, REAL_PERF, SIMPLER_PERF
TASK = "google_robot_pick_coke_can"
def get_results(policy):
    real_results = []
    simpler_results = []
    for k in SIMPLER_PERF.keys():
        try:
            real_results.append(REAL_PERF[k][policy])
            simpler_results.append(SIMPLER_PERF[k][policy])
        except:
            continue
    return np.array(real_results), np.array(simpler_results)

if __name__ == "__main__":
    print("======= SIMPLER Evaluation =======\n")

    y = np.array([0.87, 0.7333333333333334, 0.5866666666666668, 0.03666666666666667])
    x = np.array([0.8533333333333332, 0.9199999999999999, 0.7599999999999999, 0.13333333333333333])
    # Create the plot
    fig = go.Figure()
    # results = get_results("rt-1-converged")
    # Add scatter plots with custom markers
    fig.add_trace(go.Scatter(
        x=[x[0]],
        y=[y[0]],
        mode='markers',
        name='RT-1 (Converged)',
        marker=dict(
            symbol='cross',  # Cross marker
            size=20,
            color='rgb(141, 160, 203)', # Bright blue
            line=dict(width=1, color='white')  # White edge
        )
    ))

    # results = get_results("rt-1-15")
    # print(results)
    fig.add_trace(go.Scatter(
        x=[x[1]],
        y=[y[1]],
        mode='markers',
        name='RT-1 (15%)',
        marker=dict(
            symbol='square',  # Circle marker
            size=20,
            color='rgb(252, 141, 98)',  # Bright orange
            line=dict(width=1, color='white')  # White edge
        )
    ))

    # results = get_results("rt-1-x")
    fig.add_trace(go.Scatter(
        x=[x[2]],
        y=[y[2]],
        mode='markers',
        name='RT-1-X',
        marker=dict(
            symbol='diamond',  # Square marker
            size=20,
            color='rgb(231, 138, 195)',  # Bright pink 
            line=dict(width=1, color='white')  # White edge
        )
    ))

    # results = get_results("rt-1-begin")
    fig.add_trace(go.Scatter(
        x=[x[3]],
        y=[y[3]],
        mode='markers',
        name='RT-1 (Begin)',
        marker=dict(
            symbol='x',  # Rotated cross marker
            size=20,
            color='rgb(102,194,165)',  # Bright green
            line=dict(width=1, color='white')  # White edge
        )
    ))

    slope, intercept = np.polyfit(x, y, 1)
    y_line = slope * x + intercept

    fig.add_trace(go.Scatter(
        x=x,
        y=y_line,
        mode='lines',
        line=dict(color='black', dash='dash', width=2),
        showlegend=False  # Exclude from legend
    ))


    # Add annotations
    # fig.add_annotation(
    #     x=0.5,
    #     y=0.5,
    #     text="MMRV = 0.031 ↓<br>r = 0.976 ↑",
    #     showarrow=False,
    #     font=dict(size=12, color="black")
    # )

    # Update layout for better visualization
    fig.update_layout(
        title="Pick Coke Can",
        xaxis_title="Real success rate",
        yaxis_title="SIMPLER-VisMatch success rate",
        xaxis=dict(range=[0.0, 1.0], showgrid=True, gridcolor='lightgray'),
        yaxis=dict(range=[0.0, 1.0], showgrid=True, gridcolor='lightgray'),
        plot_bgcolor='white',  # White background
        paper_bgcolor='white',  # White frame
        showlegend=True,
        legend=dict(
            orientation='h',  # Horizontal legend
            yanchor='bottom',  # Anchor legend at the bottom
            y=-0.3,  # Position legend below the plot
            xanchor='center',  # Center legend horizontally
            x=0.5
        ),
        width=500,  # Square frame (width and height set to the same value)
        height=500,
        margin=dict(l=50, r=50, b=100, t=50)  # Adjust bottom margin for legend
    )

    # Save the plot as a static image file
    pio.write_image(fig, 'plot.png', scale=2)  # Save as PNG with high resolution