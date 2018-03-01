# Welcome to the Domestic-Water-Heating wiki!

The Domestic Water Heating is a repository which has a tool for generating hourly residencial hot water draw profiles. The profile is generated based on probability distributions for shower, sink and dishwasher events.
After the profile is generated the climate data is loaded in order to model a solar collector and the mains water temperature.
4 different alternatives considering and without considering a solar collector are compared to a Base case.
* Electric resistance storage
* Heat pump
* Gas tankless
* Gas storage

Daily, monthly and annual energy consumption, monthly and annual cost, Payback, Internal Rate of Return (IRR) and Net Present Value (NPV) are presented for each alternative considering 2 different tariffs.

It takes as input the number of occupants of the desired house to model.
The model outputs 11 graphs with each run:
* Daily hot water consumption
* Hourly hot water consumption for a random day of the year
* Heat Pump's COP throughout the year
* Collector's efficiency throughout the year
* Daily energy consumption comparison for the scenarios 
* Monthly energy consumption comparison for the scenarios 
* Monthly money cost for the scenarios
* Annual energy consumption comparison for the scenarios 
* Annual money cost comparison for the scenarios 
* Payback and IRR
* NPV

The variability of the model is studied for a identical case which is run 500 times and presents the standard deviation of each alternative as a percentage of the average

The variation of energy consumption per alternative is also studied when the consumption pattern and the amount of people per house changes.

The modules are separated for easier understanding and the ipython notebook includes a step by step explanation in Spanish.
