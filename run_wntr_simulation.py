import wntr
import matplotlib.pyplot as plt

def simulate_leak():
    # ✅ Use built-in Net3 model (no need for .inp file)
    wn = wntr.network.models.networks.net3()

    # ✅ Choose a valid node from Net3 for the leak
    leak_node = '121'  # You can change this to any node from wn.junction_name_list
    start_time = 2 * 3600  # Leak starts at 2 hours
    end_time = 8 * 3600    # Leak ends at 8 hours
    area = 0.0001          # Leak area in m²
    discharge_coeff = 0.75

    # ✅ Add a leak to the node
    wn = wntr.morph.leak.add_leak(wn, leak_node, area, discharge_coeff, start_time, end_time)

    # ✅ Run the simulation
    sim = wntr.sim.WNTRSimulator(wn)
    results = sim.run_sim()

    # ✅ Get pressure and flowrate results
    pressure = results.node['pressure']
    flowrate = results.link['flowrate']

    return pressure, flowrate

if __name__ == "__main__":
    pressure, flow = simulate_leak()

    # ✅ Plot pressure at the leak node
    node_to_plot = '121'
    pressure[node_to_plot].plot()
    plt.title(f'Pressure at Node {node_to_plot}')
    plt.xlabel('Time (s)')
    plt.ylabel('Pressure (m)')
    plt.grid(True)
    plt.show()
