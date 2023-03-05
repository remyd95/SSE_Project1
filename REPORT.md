---
author: Rover van der Noort, Martijn Smits, Remy Duijsens, Dajt Mullaj
title: "The Effect of Different Power Profiles on Energy Consumption and Runtime Performance in Machine Learning Applications"
date: 03/03/2023
summary: "Training neural networks is a daily task for AI engineers. In this study, we evaluate the effects of different power profiles on the performance and energy consumption of a neural network training benchmark. Our results show that the power-save profile causes the benchmark to use significantly less energy than the other power profiles. The difference in runtime is statistically significant but in absolute measure not practically relevant for this use case."
---


## Introduction

Climate change is an important research topic and specifically in the field of computer science the problem of massive power consumption persists [1, 2]. Recently many new solutions have appeared, which try to tackle this problem in a variety of ways [1, 2, 6, 9]. Popular operating systems (OS) have introduced power-saving settings as built-in features, which enable any user to activate them. It is however not directly clear how much energy these profiles save or how it affects the performance of a system.

The popularity of Machine Learning (ML) models has increased parallel to the interest in sustainability [3, 7]. However, generally, these models require large quantities of energy to train and deploy [3, 5, 7, 8]. It is therefore important to create a sustainable mindset for current and new ML engineers, because they can significantly reduce the power consumption of their whole pipeline by choosing the right implementation details [7, 9]. 

[TensorFlow](https://tensorflow.org) is a widely used open-source library to create and deploy ML models. Perfzero offers a benchmark framework to test a system's performance for ML computations. Although this benchmark does not cover the hollistic pipeline of ML engineering, it can show effect of a general ML task and give an indication of any impact on the power consumption and performance.

This study investigates the impact of the Ubuntu Power Profiles on the benchmark framework for TensorFlow and could show ML developers the impact of power saving methods. This study elaborates on the studied libraries and how they will be tested, followed by the results of the experiment. This is concluded with a discussion of the findings and some further work recommendations. 

## Related Work

Ubuntu Power Profiles are built into Gnome as the [power-tools-daemon](https://gitlab.freedesktop.org/hadess/power-profiles-d), which offers three different power modes: balanced, power-saver, and performance. It performs a set of actions depending on the profile and the system's highly customizable hardware. For Intel-based machines, it uses [P-state scaling](https://www.kernel.org/doc/html/v5.17/admin-guide/pm/intel_pstat), which can utilise hardware-specific optimizations for energy consumption or performance. 

There are similar applications like power-tools-daemon, such as the open-source applications [TuneD](https://github.com/redhat-performance/tu) by RedHat, which is designed for Fedora-based systems. Another common application is [TLP](https://github.com/linrunner/TLP) by linrunner, which is specifically designed for battery power saving. All applications are fairly similar in their operations, which is why they are all incompatible to run concurrently on a single machine. 

Many Energy Profiler applications vary in their method of measurement [4]. [Powerstat](https://manpages.ubuntu.com/manpages/bionic/man8/powerstat.8.html) is a simple-to-use tool made for Ubuntu that allows to measure battery systems and systems that support Running Average Power Limit (RAPL) interfaces. [PowerTOP](https://github.com/fenrus75/powertop) is a different option designed by Intel, which is a heavy duty application for power measurements and dynamic power settings, however this could interfere with the power profile. It requires, similar to other applications [Perf](https://www.man7.org/linux/man-pages/man1/perf.1.html) and [Likwid](https://github.com/RRZE-HPC/likwid) more callibration and configuration. Lastly, [nvidia-smi](https://developer.nvidia.com/nvidia-system-management-interface) allows us to specifically test NVIDIA gpu's with higher accuracy.

## Methodology
Multiple factors play a role in the power consumption rate of a computer. To increase the accuracy of the results, we need to minimise the effect of these factors. Therefore we will prepare the environment (both internal and external) before running the tests, we will do that as follows:  

- **Background processes** use power and can also cause spikes in energy consumption. This will lead to inaccurate measurements of the actual power consumption of the benchmarking software. Therefore we kill all non-essential background tasks during the test, this includes disabling notifications. On top of that, we randomise the order in which the tests are run. This decreases the chance of unforeseen background tasks running only during one specific scenario.  
- **Battery health** can affect power consumption and therefore we do not run the test in battery mode, but use a stationary desktop. 
- **External devices** can also impact battery life, therefore we run the tests with no external devices plugged in.  
- **Temperature** plays a role in the energy consumption of a system and for consistency we run all the tests at room temperature. We take thirty seconds breaks between runs of the benchmark to give the system components time to cool down. Before running any of the tests we run a Fibonacci sequence for one minute to warm up the CPU and a benchmark for roughly 40 seconds to warm up the GPU, this is because we cannot fully cool down the components for each of the tests.  
- **Other external factors**, such as the surface on which the computer stands, may also affect power consumption. Therefore we will gather all the results in the same environment on the same device.

The tests consist of three different scenarios. There are three power save modes for which we test the power consumption of an idle system and the consumption of running the benchmark. The power profiles are as follows:  

- **Power saver:** This profile is designed to minimise power consumption by reducing the CPU speed, disabling some hardware features, and other optimisations.  

- **Balanced:** This is the default profile that provides a good balance between performance and power consumption.  

- **High performance:** This profile maximises performance by increasing the CPU speed, disabling some power-saving features, and other optimisations.

We measure the *total power consumption* to run the benchmark. To further decrease the potential effect of undesired factors, we take some additional measures. First, we run each scenario 30 different times and average the results. Secondly, we automate the full test, so that manual mistakes are eliminated.

The full automated test sequence works as follows. We initialise thirty experiments per power mode and shuffle these randomly. Then we warmup the system in balanced power mode. As mentioned earlier we do this by running fibonacci for the CPU and the benchmark for the GPU. After that we run the experiments in the shuffeled order. For each experiment we start the correct powermode. Then we start the power measurement, for this we use RAPL for more accurate results. We then start the benchmark and gather the results. After this we do a thirty second cooldown and then continue to the next experiment. After running the benchmark on each power-profile mode for thirty times, we process the results.

## Results
The experiments were executed on an HP ZBook Studio G4 with an Intel i7-7700HQ processor and an NVIDIA Quadro M1200 Mobile with 8GB RAM. The operating system used was Ubuntu 22.04.2. In total 90 experiments, 30 for each power mode, were conducted in a randomly shuffled order. The benchmark workload that was used is a synthetic neural network training job on the Cifar-10 dataset on a Resnet model. This workload was controlled by the Perfzero benchmark tool, which is designed for Tensorflow performance benchmarks. Tensorflow has been configured to use the available GPU in the system to resemble the setup that is most common for AI engineers. The energy consumption was measured using the Powerstat tool which is based on the Intel RAPL measurement feature. 

 
The results obtained for each profile are presented in the following table.


TABLE OF RESULTS
 

### Exploratory Analysis

We visualized the data to gain some insights into its structure. As can be seen in Figure (ADD FIGURES ERRORBARS), it seems that the data is structured as expected, with the Powersaver profile being the most energy efficient and costly in terms of time and the Performance profile being the fastest but least energy efficient. 

![lineplots](https://raw.githubusercontent.com/remyd95/SSE_Project1/main/images/lineplots.png)
*Figure 1. (a) Energy consumption in Joule of each power profile; (b) Processing time in seconds of each power profile; (c) Time vs Energy of each profile displayed in order to identify the Pareto frontier.*

However to draw any conclusive interpretation we need to understand the statistical significance of the results. To do that we explored the data distribution using a box plot and a violin plot.  

![boxplots_violinplots](https://raw.githubusercontent.com/remyd95/SSE_Project1/main/images/boxplot_violinplot.png)

*Figure 2. (a-b) Boxplots and (c-d) Violinplots to identify outliers and the distributions of the energy consumptions and processing times of the power profiles.*

To run the necessary test for statistical significance we needed to confirm that the data is normal. As seen in the distribution plots this is hard to conclude just from the visualizations.

![kde](https://raw.githubusercontent.com/remyd95/SSE_Project1/main/images/kde.png)

*Figure 3. Kernel density plots to further highlight the nature of the data distributions for energy (a) and time (b) consumptions of each profile.*


We therefore run a Shapiro-Wilk test to confirm normality. The p-values obtained from the test are displayed in the following table.

 

TABLE TO BE INSERTED

 

As can be seen not all data is normally distributed. We therefore tried to remove the outliers using z-scores, and removing points with a score higher than three standard deviations. However, only the time data for the Balanced profile became normal after outlier removal. We therefore performed a sanity check by rerunning the whole experiment, however, we got similar results regarding the data normality distributions as shown in Table X.

 

TABLE WITH SHAPIRO TEST FOR FIRST EXPERIMENT

 

Therefore we moved forward concluding that not all data distributions are normal. 

 

### Statistical Significance and Effect Size 

 

We checked the statistical significance of the differences between the three profiles by using a two-sided Welsch t-test or Manney-Wittney U-test depending on the normality of the data. 

 

ADD TABLE OF RESULTS 

 

Of these results, only the difference in energy consumption between the Balanced and Performance profile is not significant. We therefore moved to check first the difference in medians between the energy consumption of the Performance and Powersaver profile, which is 387 J, and between the Balanced and Powersaver profile, which is 386 J. In both cases, the difference is of three orders of magnitude. The difference in time, instead, is always below 1 second. 

 

ADD A TABLE WITH DIFFERENCES 

 

We also computed the pair percentages as reported in the following table. 

 

ADD TABLE PAIR PERCENTAGES

 

Finally, we computed the Choen's or Cliff's delta, again depending on the normality of the data. Each delta result indicates that the difference of the distributions is large, in the case of the times of the Balanced and Performance profile, for example, Choen's data indicates that the results are generally separated by almost an entire standard deviation.

<!-- argue about practical signifiance (This is in the discussion or as a new section in results not sure)-->


## Discussion


The presented work comes with a couple of limitations. The Perfzero TensorFlow benchmark tool requires an internet connection to be able to run. An Internet connection can cause serious distortions in the measurement, for instance, due to background processes that need to sync. Another limitation related to the benchmark tool is that we had to use a synthetic benchmark tool to be able to keep the experiments short. Real-world machine learning training jobs in common scenarios can take several hours to complete. In an ideal experiment, such a real-world training job would be the best choice. Another limitation is that ultimately, the effects of the unwanted side factors cannot be removed. These factors, especially in our setup, can only be minimised. Lastly, the gathered data does not follow a normal distribution for all power mode results. However, it is known that when working with AI applications, the outcome is rarely deterministic and a normal distribution is therefore not feasible.


<!--

- energy: power-saver not normal

- time: power-saver and performance not normal -->


In the context of our research, the power save mode is the most energy-efficient. However, in a real scenario, a user might not do the same preparation as we did. They might have their screen turned on, or unnecessary background processes running. As stated earlier, looking at the hollistic pipeline for ML application is important [7]. Since the power-save mode has an overall longer runtime, it could be possible that with additional energy-consuming processes running for an overall longer time, that power-save mode might be more energy-consuming than the other energy profiles. Extra research needs to be conducted to prove or disprove this hypothesis.

<!-- 
- Limitation -> wifi
- Limitation -> synth benchmark, real benchmark
- Limitation -> unwanted factors cannot be removed, only minimised
- Hard to get normal distr. when working with ML applications 
- energy: power-saver not normal
- time: power-saver and performance not normal
- Discussion point: In the context of our research the powersave mode is the most beneficial, however in a real scenario the user might have their display on and background processes running, therefore the longer runtime of the task might actually consume more energy overall 
-->


## Conclusion

In this work, we have motivated the need for energy-efficient solutions, especially in energy-intensive domains like ML. One easy way to adjust the power usage on laptops is by applying different power profiles. Three different power profiles for Ubuntu have been benchmarked on a ML training benchmark job. The experiments measured both energy consumption and the runtime of the training job. The results of the experiments show that the power-save profile consumes significantly less energy than the balanced and performance profiles. While the runtime shows the same significant difference, the practical significance is less applicable. The small increase in runtime compared to the large decrease in energy consumption makes the power-save profile a viable energy-aware choice for ML engineers. The experiments were repeated with Tensorflow without GPU support. A similar energy pattern emerged with again little practical significance in the difference in runtime across all power modes. Further research can extend this work by repeating the experiments in a more controlled setting. Furthermore, instead of short synthetic benchmarks, real benchmarks can be used to simulate real-world ML mode training scenarios. At last, different systems can be evaluated including operating systems, different models and datasets, and different types of hardware including hardware that is more commonly by ML engineers.


## References
[1] Hayri Acar, G ̈ulfem I Alptekin, Jean-Patrick Gelas, and Parisa Ghodous.
The Impact of Source Code in Software on Power Consumption. Interna-
tional Journal of Electronic Business Management, 14:42–52, 2016.


[2] Coral Calero and Mario Piattini. Introduction to Green in Software Engi-
neering, pages 3–27. Springer International Publishing, Cham, 2015.


[3] Eva Garc ́ıa-Mart ́ın, Crefeda Faviola Rodrigues, Graham Riley, and H ̊akan
Grahn. Estimation of energy consumption in machine learning. Journal of
Parallel and Distributed Computing, 134:75–88, 2019.


[4] Erik Jagroep, Jan Martijn E. M. van der Werf, Slinger Jansen, Miguel Fer-
reira, and Joost Visser. Profiling energy profilers. In Proceedings of the 30th
Annual ACM Symposium on Applied Computing, SAC ’15, page 2198–2203,
New York, NY, USA, 2015. Association for Computing Machinery.


[5] Mohit Kumar, Xingzhou Zhang, Liangkai Liu, Yifan Wang, and Weisong
Shi. Energy-efficient machine learning on the edges. In 2020 IEEE
International Parallel and Distributed Processing Symposium Workshops
(IPDPSW), pages 912–921, 2020.3


[6] Stefan Naumann, Markus Dick, Eva Kern, and Timo Johann. The greensoft
model: A reference model for green and sustainable software and its engi-
neering. Sustainable Computing: Informatics and Systems, 1(4):294–304,
2011.

[7] Carole-Jean Wu, Ramya Raghavendra, Udit Gupta, Bilge Acun, Newsha
Ardalani, Kiwan Maeng, Gloria Chang, Fiona Aga, Jinshi Huang, Charles
Bai, Michael Gschwind, Anurag Gupta, Myle Ott, Anastasia Melnikov, Sal-
vatore Candido, David Brooks, Geeta Chauhan, Benjamin Lee, Hsien-Hsin
Lee, Bugra Akyildiz, Maximilian Balandat, Joe Spisak, Ravi Jain, Mike
Rabbat, and Kim Hazelwood. Sustainable ai: Environmental implications,
challenges and opportunities. In D. Marculescu, Y. Chi, and C. Wu, editors,
Proceedings of Machine Learning and Systems, volume 4, pages 795–813,
2022.

[8] Wenninger, Simon; Kaymakci, Can; Wiethe, Christian; Römmelt, Jörg; Baur, Lukas; Häckel, Björn; and Sauer, Alexander, "How Sustainable is Machine Learning in Energy Applications? – The Sustainable Machine Learning Balance Sheet" (2022). Wirtschaftsinformatik 2022 Proceedings.

[9] SA Budennyy, VD Lazarev, NN Zakharenko, AN Korovin, OA Plosskaya,
DV Dimitrov, VS Akhripkin, IV Pavlov, IV Oseledets, IS Barsola, et al.
Eco2ai: carbon emissions tracking of machine learning models as the first
step towards sustainable ai. In Doklady Mathematics, pages 1–11. Springer,
2023.