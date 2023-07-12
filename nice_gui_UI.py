import threading
from nicegui import ui, app

class Device(dict):
    def __init__(self, name, peak_power, daily_consumption):
        self['device_name'] = name
        self['peak_power'] = peak_power
        self['daily_consumption'] = daily_consumption

potential_consumers = [
    Device("Fridge", 100, 50),
    Device("Microwave", 2500, 50),
    Device("Kettle", 2000, 50),
    Device("Oven", 3000, 150),
    Device("Laptop", 150, 30),
    Device("TV", 300, 500),
    Device("PC", 600, 700),
]  
class NiceGuiUI:

    def start_UI(self):
        model = {'maximum_peak_power': 0}

        potential_consumers_dict = dict()
        for index in range(len(potential_consumers)):
            potential_consumers_dict[index] = potential_consumers[index]['device_name']

        ui.label('PV System Planner').style('color: #6E93D6; font-size: 200%; font-weight: 300')
        ui.label('Add all your electric devices.')

        selected_consumers_list = []
        selected_consumers_table = ui.aggrid({
            'columnDefs': [
                {'headerName': 'Device name', 'field': 'device_name', 'checkboxSelection': True},
                {'headerName': 'Peak power', 'field': 'peak_power'},
                {'headerName': 'Daily consumption', 'field': 'daily_consumption'},
            ],
            'rowData': selected_consumers_list,
            'rowSelection': 'multiple',
        }).classes('max-h-40').props('id=selected_consumers_table')

        def selected_consumers_table_update():
            model.update(maximum_peak_power=sum([device["peak_power"] for device in selected_consumers_list]))
            selected_consumers_table.update()

        add_device_dropdown_selection_value = dict()
        add_device_dropdown_selection_value['value'] = 0

        def add_selected_device_to_consumers():
            selected_consumers_list.append(potential_consumers[add_device_dropdown_selection_value['value']])
            selected_consumers_table_update()

        def remove_device_from_consumers(device: dict):
            selected_consumers_list.remove(device)

        def remove_last_device_from_consumers():
            selected_consumers_list.pop()
            selected_consumers_table_update()

        async def remove_selected_devices_from_consumers():
            rows = await selected_consumers_table.get_selected_rows()
            if rows:
                for row in rows:
                    remove_device_from_consumers(row)
                    ui.notify(f"{row['device_name']} removed from list")
                selected_consumers_table_update()
            else:
                ui.notify('No rows selected.')

        with ui.row():
            remove_last_device_button = ui.button('Remove last device', on_click=remove_last_device_from_consumers).props('id=remove_last_device_button')
            remove_selected_devices_button = ui.button('Remove selected device', on_click=remove_selected_devices_from_consumers).props('id=remove_selected_devices_button')

        add_device_dropdown_selection = ui.select(potential_consumers_dict, value=add_device_dropdown_selection_value)\
            .bind_value(add_device_dropdown_selection_value, 'value').style('color: #6E93D6; font-size: 150%; font-weight: 300; border: 1px gray').props('id=add_device_dropdown_selection')
        peak_power_label = ui.label(f"Peak power: {potential_consumers[add_device_dropdown_selection_value['value']]['peak_power']}")\
            .bind_text_from(add_device_dropdown_selection_value, 'value', backward=lambda t: f"Peak power: {potential_consumers[int(t)]['peak_power']} W").props('id=peak_power_label')
        daily_consumption_label = ui.label(f"Daily consumption: {potential_consumers[add_device_dropdown_selection_value['value']]['daily_consumption']}")\
            .bind_text_from(add_device_dropdown_selection_value, 'value', backward=lambda t: f"Daily consumption: {potential_consumers[int(t)]['daily_consumption']} Wh").props('id=daily_consumption_label')
        add_selected_device_button = ui.button('Add device', on_click=add_selected_device_to_consumers).props('id=add_selected_device_button')

        ui.label('Summary').style('color: #6E93D6; font-size: 150%; font-weight: 300')
        with ui.row():
            ui.icon('power', color='primary').style('color: #6E93D6; font-size: 150%; font-weight: 300;')
            ui.label("Maximum peak power: ")
            maximum_peak_power_label = ui.label().style('color: #6E93D6; font-size: 150%; font-weight: 300;').bind_text_from(model, 'maximum_peak_power').props('id=maximum_peak_power_label')

        ui.button('shutdown', on_click=app.shutdown).props('id=shutdown_button')
        ui_run_kwargs = {"port": 8081, "show": True, "reload": False}
        self.server_thread = threading.Thread(target=ui.run, kwargs=ui_run_kwargs)
        self.server_thread.start()

    def stop_UI(self):
        app.shutdown()

if __name__ == "__main__":
    nice_gui = NiceGuiUI()
    nice_gui.start_UI()
