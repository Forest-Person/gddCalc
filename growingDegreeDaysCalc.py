import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

# Full crop data with GDD requirements
crops_data = {
    "Egyptian Onions": {"base_temp": 40, "total_gdd": 1800},
    "Parsnips": {"base_temp": 40, "total_gdd": 1200},
    "Leeks": {"base_temp": 40, "total_gdd": 900},
    "Cabbage": {"base_temp": 50, "total_gdd": 1200},
    "Arugula": {"base_temp": 40, "total_gdd": 300},
    "Rye": {"base_temp": 32, "total_gdd": 1000},
    "Fava Beans": {"base_temp": 40, "total_gdd": 1200},
    "Oats": {"base_temp": 40, "total_gdd": 1400},
    "Vetch": {"base_temp": 40, "total_gdd": 600},
    "Spinach": {"base_temp": 40, "total_gdd": 400},
    "Carrots": {"base_temp": 45, "total_gdd": 1300},
    "Kale": {"base_temp": 40, "total_gdd": 900},
    "Radishes": {"base_temp": 40, "total_gdd": 400},
    "Mustard Greens": {"base_temp": 45, "total_gdd": 800},
    "Broccoli": {"base_temp": 50, "total_gdd": 1000},
    "Cauliflower": {"base_temp": 50, "total_gdd": 1100},
    "Brussels Sprouts": {"base_temp": 50, "total_gdd": 1500},
    "Collard Greens": {"base_temp": 50, "total_gdd": 900},
    "Turnips": {"base_temp": 45, "total_gdd": 900},
    "Winter Wheat": {"base_temp": 32, "total_gdd": 1100},
    "Barley": {"base_temp": 32, "total_gdd": 1200},
    "Buckwheat": {"base_temp": 40, "total_gdd": 600},
    "Clover": {"base_temp": 40, "total_gdd": 800},
    "Field Peas": {"base_temp": 40, "total_gdd": 1000},
    "Triticale": {"base_temp": 32, "total_gdd": 900},
    "Hairy Vetch": {"base_temp": 32, "total_gdd": 750},
    "Salsify": {"base_temp": 40, "total_gdd": 1200},
    "Collards": {"base_temp": 50, "total_gdd": 900},
    "Parsley": {"base_temp": 50, "total_gdd": 800},
    "Potatoes": {"base_temp": 45, "total_gdd": 1200},
    "Rutabagas": {"base_temp": 45, "total_gdd": 1000},
    "Radish": {"base_temp": 40, "total_gdd": 400},
    "Jerusalem Artichoke": {"base_temp": 45, "total_gdd": 1200},
    "Sunflower": {"base_temp": 50, "total_gdd": 1400},
    "Quinoa": {"base_temp": 45, "total_gdd": 1200},
}

class GDDCalculatorApp(App):
    def build(self):
        # Root layout
        root = BoxLayout(orientation='vertical')

        # Scrollable list of crops
        scroll_view = ScrollView(size_hint=(1, 0.6))
        grid_layout = GridLayout(cols=1, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        # Create buttons for each crop in the crops_data dictionary
        for crop in crops_data.keys():
            btn = Button(text=crop, size_hint_y=None, height=75,font_size=60)
            btn.bind(on_press=self.on_crop_select)
            grid_layout.add_widget(btn)

        scroll_view.add_widget(grid_layout)

        # Input fields for high and low temperatures
        self.temp_input_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        self.high_temp_input = TextInput(hint_text='High Temp (°F)', input_filter='float', multiline=False)
        self.low_temp_input = TextInput(hint_text='Low Temp (°F)', input_filter='float', multiline=False)
        self.temp_input_layout.add_widget(self.high_temp_input)
        self.temp_input_layout.add_widget(self.low_temp_input)

        # Button to calculate GDD
        self.calculate_btn = Button(text='Calculate GDD', size_hint=(1, 0.2))
        self.calculate_btn.bind(on_press=self.calculate_gdd)

        # Label for displaying results
        self.result_label = Label(text='Select a crop and enter temperatures.', size_hint=(1, 0.2))

        # Add widgets to root layout
        root.add_widget(scroll_view)
        root.add_widget(self.temp_input_layout)
        root.add_widget(self.calculate_btn)
        root.add_widget(self.result_label)

        return root

    def on_crop_select(self, instance):
        self.selected_crop = instance.text
        self.result_label.text = f'Selected Crop: {self.selected_crop}. Enter high and low temps.'

    def calculate_gdd(self, instance):
        # Get high and low temps from input
        try:
            high_temp = float(self.high_temp_input.text)
            low_temp = float(self.low_temp_input.text)
        except ValueError:
            self.show_popup("Invalid Input", "Please enter valid temperatures.")
            return

        # Calculate daily GDD
        base_temp = crops_data[self.selected_crop]["base_temp"]
        daily_gdd = max(0, ((high_temp + low_temp) / 2) - base_temp)

        # Get total GDD required and estimate days to harvest
        total_gdd = crops_data[self.selected_crop]["total_gdd"]
        estimated_days = round(total_gdd / daily_gdd) if daily_gdd > 0 else "N/A"

        # Display results
        self.result_label.text = (
            f"{self.selected_crop}\n"
            f"Daily GDD: {daily_gdd:.2f}\n"
            f"Total GDD Required: {total_gdd}\n"
            f"Estimated Days to Harvest: {estimated_days}"
        )

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical')
        popup_label = Label(text=message)
        popup_button = Button(text='Close', size_hint=(1, 0.3))
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(popup_button)
        popup = Popup(title=title, content=popup_layout, size_hint=(0.7, 0.3))
        popup_button.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    GDDCalculatorApp().run()