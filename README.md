# Coffee Industry
Ironhack | Data Analytics End-to-End | Final Project | Coffee

 <h3 align="center">Unraveling the Global Coffee Trade: Strategic Insights for Colombian Exporters</h3>

 <p align="center">
    <img src="README_images\morning_coffee.jpeg" alt="morning_coffee" width="400" >
</div>

<p align="center"><i>"As long as there was coffee in the world, how bad could things be?" - Cassandra Clare.</i>

## Table of contents
- [Introduction](#introduction)
- [Business Understanding](#business-understanding)
- [Data Mining](#data-mining)
- [Data Wrangling](#data-wrangling)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [Theory-Specific Analysis](#theory-specific-analysis)
  - [Hypothesis 1](#hypothesis-1-sharks-hate-surfers-especially-male-surfers)
  - [Hypothesis 2](#hypothesis-2-sharks-from-australia-are-les-aggressive-than-american-sharks)
  - [Hypothesis 3](#hypothesis-3-sharks-are-not-attacking-more-than-beforemaybe-we-are-the-problem)
- [Final thoughts](#final-thoughts)

## Introduction
Hi visitor! and welcome to my Ironhack Data Analytics capstone project! 

This end-to-end data analytics project is the showcase of the skills and knowledge I've acquired during the Ironhack Bootcamp 2024. Through this work, I aim to demonstrate my expertise as a market researcher and my ability to tackle real-world problems using data analysis resources. This project not only highlights my proficiency in business acumen and as a market researcher; but it also expose my skills in data gathering, manipulation, analytics and visualisations. This project also serves as a tool to learn about the heart-warming Coffee Industry and its impact in our society.

 <p align="center">
    <img src="README_images\first_day.webp" width="400" >
</div>

## Business Understanding

Coffee is not just a popular beverage; it’s a crucial global commodity that supports the livelihoods of millions, particularly in developing countries. In 2023, global coffee consumption reached approximately 693.3 billion cups, meaning each adult on Earth, on average, consumed about one-third of a cup daily. If these cups were lined up, they would circle the globe 1,383 times.

Coffee is more than just a daily ritual; it’s a powerhouse in agricultural production. The world produced over 10 million metric tons (10 billion kilograms) of coffee beans in 2023, enough to fill 2,000 Olympic-sized swimming pools. Over 90% of this production occurs in developing nations, with Brazil leading as the largest producer, contributing nearly 4 million metric tons (3.9 billion kilograms) of coffee.

 <p align="center">
    <img src="README_images\beans_plant_coffee.jpeg" width="400" >
</div>

Coffee cultivation is labor-intensive, requiring constant human attention from planting to harvesting. This makes it a crucial source of employment in many developing countries, though it also creates economic pressures and uncertainty due to its vulnerability to climate conditions.

Despite being produced mainly in developing nations, the bulk of coffee is consumed in industrialized countries. In 2023, Europe remained the largest consuming region, with 3.2 million metric tons consumed.

 <p align="center">
    <img src="README_images\smile_its_coffee.webp" width="400" >
</div>

The global coffee market, valued at $495 billion, is economically significant, comparable to the GDP of countries like Belgium or Thailand. It is larger than industries such as video games and luxury goods, and similar in size to the revenues of major multinational corporations like Apple and Amazon. The coffee industry plays a substantial role not only as a daily commodity but also as a major player in the global economy.


*Notes:*
- All market coffee figures are sourced from the [International Coffee Organization (ICO)](https://icocoffee.org/) [Coffee Report and Outlook - December 2023](https://icocoffee.org/resources/public-market-information/).

Comparative Figures:
- Belgium GDP: ~$582 billion.
- Thailand GDP: ~$500 billion.
- Global Video Game Industry: ~$200 billion.
- Luxury Goods Market: ~$300 billion.
- Apple’s Revenue (2023): ~$394 billion.
- Amazon’s Revenue (2023): ~$514 billion.

## Data Mining

### Kaggle: Coffee Dataset

To understand the trends and growth of the global coffee market, I will analyze historical data from the following *Kaggle* [Coffee Dataset](https://www.kaggle.com/datasets/michals22/coffee-dataset/data?select=Coffee_domestic_consumption.csv). This repository contains a set of datasets with information about coffee production, consumption, and trade since 1990 up to 2020. All data within these datasets has been extracted from the official [International Coffee Organization ICO](https://icocoffee.org/) website.

 <p align="center">
    <img src="README_images\Kaggle.png" width="400" >
</div>


### UN ComTrade Database: Coffee

To understand the trends and growth of the global coffee market, I will analyze the supply, demand, and trade dynamics of the main industry players by 2023, using the top producers and exporters as referenced in the annual report of the [International Coffee Organization ICO](https://icocoffee.org/). 

 <p align="center">
    <img src="README_images\ICO.png" width="400" >
</div>

The top three coffee producers and exporters worldwide are Brazil, Vietnam, and Colombia. Therefore, I will begin by analyzing the dynamics of these three markets. To accomplish this, I extracted data from the [UN ComTrade Database](https://comtradeplus.un.org/), the global trade data platform from the [United Nations](https://www.un.org/). I selected the target countries and exported data related to overall exports and specifically coffee exports.

 <p align="center">
    <img src="README_images\UN_Comtrade.png" width="400" >
</div>

## Data Wrangling
