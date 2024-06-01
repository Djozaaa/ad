import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

# Ініціалізація додатку Dash
app = dash.Dash(__name__, external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'])

# Початкові значення параметрів
initial_values = {
    'amplitude': 1.0,
    'frequency': 1.0,
    'phase': 0.0,
    'noise_mean': 0.0,
    'noise_covariance': 0.1,
    'show_noise': True,
    'filter_order': 3,
    'filter_cutoff': 0.1,
    'show_filtered': True
}

# Параметри часу
t = np.linspace(0, 1, 1000)

# Власний фільтр
def custom_filter(signal, order, cutoff):
    b = np.ones(order) / order
    a = [1]
    filtered_signal = np.convolve(signal, b, mode='same')
    return filtered_signal

# Початковий шум
noise = np.random.normal(initial_values['noise_mean'], np.sqrt(initial_values['noise_covariance']), len(t))

def generate_signals(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise, filter_order, filter_cutoff, show_filtered):
    signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), len(t))
    noisy_signal = signal + noise if show_noise else signal
    filtered_signal = custom_filter(noisy_signal, filter_order, filter_cutoff) if show_filtered else signal
    
    return signal, noisy_signal, filtered_signal

# Візуалізація інтерфейсу
app.layout = html.Div([
    html.Div([
        html.H1("Harmonic Signal with Noise and Custom Filter"),
    ], className='text-center'),

    dcc.Graph(id='signal-plot'),
    
    html.Div([
        html.Div([
            html.Label('Amplitude'),
            dcc.Slider(
                id='amplitude-slider', 
                min=0.1, max=5.0, step=0.1, value=initial_values['amplitude'],
                marks={i: str(i) for i in np.arange(0.1, 5.1, 1.0)}
            ),
            html.Label('Frequency'),
            dcc.Slider(
                id='frequency-slider', 
                min=0.1, max=5.0, step=0.1, value=initial_values['frequency'],
                marks={i: str(i) for i in np.arange(0.1, 5.1, 1.0)}
            ),
            html.Label('Phase'),
            dcc.Slider(
                id='phase-slider', 
                min=0.0, max=2*np.pi, step=0.1, value=initial_values['phase'],
                marks={i: f'{i:.1f}' for i in np.arange(0.0, 2*np.pi+0.1, np.pi/2)}
            ),
        ], className='col'),
        
        html.Div([
            html.Label('Noise Mean'),
            dcc.Slider(
                id='noise-mean-slider', 
                min=-1.0, max=1.0, step=0.1, value=initial_values['noise_mean'],
                marks={i: str(i) for i in np.arange(-1.0, 1.1, 0.5)}
            ),
            html.Label('Noise Covariance'),
            dcc.Slider(
                id='noise-covariance-slider', 
                min=0.01, max=1.0, step=0.01, value=initial_values['noise_covariance'],
                marks={i: f'{i:.2f}' for i in np.arange(0.01, 1.01, 0.2)}
            ),
            html.Label('Filter Order'),
            dcc.Slider(
                id='filter-order-slider', 
                min=1, max=10, step=1, value=initial_values['filter_order'],
                marks={i: str(i) for i in range(1, 11)}
            ),
            html.Label('Filter Cutoff'),
            dcc.Slider(
                id='filter-cutoff-slider', 
                min=0.01, max=0.5, step=0.01, value=initial_values['filter_cutoff'],
                marks={i: f'{i:.2f}' for i in np.arange(0.01, 0.51, 0.1)}
            ),
        ], className='col'),

        html.Div([
            dcc.Checklist(
                id='show-options',
                options=[
                    {'label': 'Show Noisy Signal', 'value': 'show_noise'},
                    {'label': 'Show Filtered Signal', 'value': 'show_filtered'}
                ],
                value=['show_noise', 'show_filtered']
            ),
            html.Button('Reset', id='reset-button', n_clicks=0)
        ], className='col'),
    ], className='row'),
])

@app.callback(
    Output('signal-plot', 'figure'),
    Input('amplitude-slider', 'value'),
    Input('frequency-slider', 'value'),
    Input('phase-slider', 'value'),
    Input('noise-mean-slider', 'value'),
    Input('noise-covariance-slider', 'value'),
    Input('filter-order-slider', 'value'),
    Input('filter-cutoff-slider', 'value'),
    Input('show-options', 'value'),
    Input('reset-button', 'n_clicks')
)
def update_plot(amplitude, frequency, phase, noise_mean, noise_covariance, filter_order, filter_cutoff, show_options, n_clicks):
    show_noise = 'show_noise' in show_options
    show_filtered = 'show_filtered' in show_options
    
    signal, noisy_signal, filtered_signal = generate_signals(
        amplitude, frequency, phase, noise_mean, noise_covariance, show_noise, filter_order, filter_cutoff, show_filtered
    )
    
    traces = [
        go.Scatter(x=t, y=signal, mode='lines', name='Signal'),
        go.Scatter(x=t, y=noisy_signal, mode='lines', name='Noisy Signal') if show_noise else go.Scatter(x=t, y=[], mode='lines', name='Noisy Signal'),
        go.Scatter(x=t, y=filtered_signal, mode='lines', name='Filtered Signal') if show_filtered else go.Scatter(x=t, y=[], mode='lines', name='Filtered Signal')
    ]
    
    layout = go.Layout(
        title='Harmonic Signal with Noise and Filtered Signal',
        xaxis={'title': 'Time'},
        yaxis={'title': 'Amplitude'},
        showlegend=True
    )
    
    return {'data': traces, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)
