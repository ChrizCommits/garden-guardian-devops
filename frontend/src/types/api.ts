export type User = {
  id: number;
  username: string;
  total_points: number;
  current_rank: string;
  current_streak: number;
  best_streak: number;
  created_at: string;
};

export type Animal = {
  id: number;
  name: string;
  category: string;
  description: string;
  image_url: string;
  safe_support_notes: string;
  unsafe_foods: string;
};

export type AnimalCard = {
  id: number;
  animal_id: number;
  animal_name: string;
  title: string;
  fact: string;
  rarity: string;
  points_value: number;
  image_url: string;
};

export type EarnedAnimalCard = AnimalCard & {
  earned_at: string;
  source_tip_id: number;
};

export type TodayTip = {
  id: number;
  title: string;
  description: string;
  month_or_season: string;
  action_instruction: string;
  safety_warning: string;
  supported_animals: Animal[];
  points_reward: number;
  possible_reward_cards: AnimalCard[];
};

export type CompleteResult = {
  awarded: boolean;
  message: string;
  points_awarded: number;
  total_points: number;
  current_rank: string;
  current_streak: number;
  best_streak: number;
  unlocked_card: AnimalCard | null;
};

export type RecentAction = {
  id: number;
  tip_id: number;
  tip_title: string;
  completed_at: string;
  points_awarded: number;
};

export type FavoriteAnimal = {
  animal_name: string;
  help_count: number;
};

export type Profile = {
  id: number;
  username: string;
  total_points: number;
  current_rank: string;
  current_streak: number;
  best_streak: number;
  collected_cards: EarnedAnimalCard[];
  recent_actions: RecentAction[];
  favorite_animals: FavoriteAnimal[];
};
