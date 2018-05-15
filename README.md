# Exploring "Downward Spiral" Effect for Video Streaming Rate Selection

This project is mainly adopted from the ideas proposed in the followin paper:

> **[Confused, Timid, and Unstable: Picking a Video Streaming Rate is Hard](http://yuba.stanford.edu/~nickm/papers/Confused_Timid_and_Unstable_Picking_a_Video_Streaming_Rate_is_Hard.pdf)** Te-Yuan Huang Nikhil Handigol Brandon Heller Nick McKeown Ramesh Johari. IMC'12


For good quality video streaming, the streaming rate (video quality) must be dynamically adapted to provide the best user experience to the viewer. If streaming rate is too high, it will cause the playback buffer to get empty frequently leading to many annoying re-buffering events. If streaming rate is too low, then naturally the viewer will experience low quality video which is definitely not good. 
    
Hence, for good viewer experience, we want:

* playback rate (video quality) to be high throughout the video play.
* least re-buffering events during the video play. 
    
Therefore the rate selection must be done based on accurate estimation of available bandwidth.

Generally, the videos of these services are hosted on standard HTTP servers in CDNs. Hence, the video streaming rate selection must be done on client side. Clients decide rate based on perceived available bandwidth. However, in presence of competing flow, rate selection algorithms have to face a weird consequence which authors call "Downward Spiral". In presence of competing flow, client perceives inaccurate bandwidth which further causes a vicious feedback loop continuously reducing the perceived bandwidth making the client to choose lower and lower playback rate (video quality). Finally, client ends up playing at much lower rate (quality) then the rate sanctioned by its fair share.

Please check our full report [here](https://github.com/HarshTrivedi/FCN-VideoStreamingProject/blob/master/report.pdf) and presentation [here](https://github.com/HarshTrivedi/FCN-VideoStreamingProject/blob/master/slides.pdf)

## Downward Spiral

The following figure summarizes the downward spiral effect:

![Downward Spiral](https://github.com/HarshTrivedi/FCN-VideoStreamingProject/raw/master/main_experiments/plots/plots-A/main_experiment.png)

## Requirements

	*  python 2.7
	*  mininet 
	*  mahimahi
	*  youtube-dl
	*  matplotlib

## Usage

The experiments are segregated in following three folders:

	*  main_experiments     [on mininet VM]
	*  cwnd_experiment      [on mininet VM]
	*  real_env_experiments [on personal machine with mahimahi]

For `main_experiments`, 

	run `chmod +x run_all_main_experiments.sh; sudo ./run_all_main_experiments.sh` in mininet VM.
	It will run all experiment settings based on `main_experiments/settings/*` files.
	The `settings_id_descriptions.txt` defines brief description for important setting ids to identify which experiment is which.

For `cwnd_experiment`, 

	run `sudo python cwnd_exp_start.py` in `cwnd_experiment` directory.
	And generate the plots with `python plot.py`

For `real_env_experiments`, 

	run `./main.sh`
	Save HAR File as video.har: Open Developer Tools on Firefox. On the Network Tab, click anywhere in the file tab. Right click and save all as har.

## Pregenerated plots

	* pregenerated plots for `main_experiments` are present in `main_experiments/plots` directory.
	* pregenerated plots for `cwnd_experiment` are present in `cwnd_experiment/plots-*` directories.
	* pregenerated plot for `real_env_experiments` is present in `real_env_experiments/plot` directory.


