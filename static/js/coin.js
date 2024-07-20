let score = 0;
let reward = 0;
let nextReward = 100;
const circle = document.getElementById('circle');
const scoreDisplay = document.getElementById('score');
const rewardDisplay = document.getElementById('reward');
const nextRewardDisplay = document.getElementById('next-reward');
const claimRewardBtn = document.getElementById('claim-reward');

circle.addEventListener('click', () => {
	score++;
	scoreDisplay.textContent = `Score: ${score}`;
	if (score >= nextReward) {
		reward++;
		rewardDisplay.textContent = `Reward: ${reward}`;
		nextReward *= 2;
nextRewardDisplay.textContent = `Next Reward: ${nextReward}`;
	}
});

claimRewardBtn.addEventListener('click', () => {
	// Telegram API integration to claim reward
});
