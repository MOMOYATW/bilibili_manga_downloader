// TODO: any

export interface BilibiliResponse<T> {
  code: number;
  msg: string;
  data: T;
}

export interface ComicDetailData {
  id: number;
  title: string;
  comic_type: number;
  page_default: number;
  page_allow: number;
  horizontal_cover: string;
  square_cover: string;
  vertical_cover: string;
  author_name: string[];
  styles: string[];
  last_ord: number;
  is_finish: number;
  status: number;
  fav: number;
  read_order: number;
  evaluate: string;
  total: number;
  ep_list: ComicEpisodeObject[];
  release_time: string;
  is_limit: number;
  read_epid: number;
  last_read_time: string;
  is_download: number;
  read_short_title: string;
  styles2: ComicTagObject[];
  renewal_time: string;
  last_short_title: string;
  discount_type: number;
  discount: number;
  discount_end: string;
  no_reward: boolean;
  batch_discount_type: number;
  ep_discount_type: number;
  has_fav_activity: boolean;
  fav_free_amount: number;
  allow_wait_free: boolean;
  wait_hour: number;
  wait_free_at: string;
  no_danmaku: number;
  auto_pay_status: number;
  no_month_ticket: boolean;
  immersive: boolean;
  no_discount: boolean;
  show_type: number;
  pay_mode: number;
  chapters: ComicChapterInfo[];
  classic_lines: string;
  pay_for_new: number;
  fav_comic_info: {
    has_fav_activity: boolean;
    fav_free_amount: number;
    fav_coupon_type: number;
  };
  serial_status: number;
  series_info: { id: number; comics: any[] };
  album_count: number;
  wiki_id: number;
  disable_coupon_amount: number;
  japan_comic: boolean;
  interact_value: string;
  temporary_finish_time: string;
  video: null;
  introduction: string;
  comment_status: number;
  no_screenshot: boolean;
  type: number;
  vomic_cvs: any[];
  no_rank: boolean;
  presale_eps: any[];
  presale_text: string;
  presale_discount: number;
  no_leaderboard: boolean;
  auto_pay_info: { auto_pay_orders: any[]; id: number };
  orientation: number;
  story_elems: ComicTagObject[];
  tags: ComicTagObject[];
  is_star_hall: number;
  hall_icon_text: string;
}

export interface ComicEpisodeObject {
  id: number;
  ord: number;
  read: number;
  pay_mode: number;
  is_locked: boolean;
  pay_gold: number;
  size: number;
  short_title: string;
  is_in_free: boolean;
  title: string;
  cover: string;
  pub_time: string;
  comments: number;
  unlock_expire_at: string;
  unlock_type: number;
  allow_wait_free: boolean;
  progress: string;
  like_count: number;
  chapter_id: number;
  type: number;
  extra: number;
  image_count: number;
}

export interface ComicTagObject {
  id: number;
  name: string;
}

export interface ComicChapterInfo {
  id: number;
  title: string;
  short_title: string;
  pay_mode: number;
  status: number;
  is_finished: number;
  cover: string;
  gold: number;
  real_gold: number;
  ord: number;
  expected_eps: number;
  msg: string;
  deadline: string;
  is_pre: number;
  is_locked: boolean;
  ep_count: number;
  unlock_type: number;
  is_vomic_pre: number;
}

export interface ComicPlusData {
  list: ComicPlusObject[];
  icon_url: string;
  comic_title: string;
}

export interface ComicPlusObject {
  isLock: boolean;
  cost: number;
  reward: number;
  item: ComicPlusItemObject;
  unlocked_item_ids: number[];
}

export interface ComicPlusItemObject {
  id: number;
  title: string;
  cover: string;
  pic: string[];
  rank: number;
  detail: string;
  limits: number;
  pic_type: number;
  pic_num: number;
  online_time: string;
  offline_time: string;
  num: number;
  type: number;
  icon: string;
  activity_url: string;
  activity_name: string;
  watermark: ComicPlusItemWatermarkObject[];
  item_ids: number[];
  no_local: boolean;
  video: ComicVideoObject | null;
  item_infos: ComicPlusItemInfoObject[];
}

export interface ComicPlusItemWatermarkObject {
  url: string;
  location: number;
  width: number;
  high: number;
  font: string;
  x: number;
  y: number;
  size: number;
  type: number;
  color: string;
}

export interface ComicPlusItemInfoObject {
  id: number;
  title: string;
}

export interface ComicVideoObject {
  id: number;
  url: string;
  cover: string;
  duration: string;
}

export interface ImageIndexData {
  path: string;
  images: ImageObject[];
  last_modified: string;
  host: string;
  video: ImageVideoObject;
}

export interface ImageObject {
  path: string;
  x: number;
  y: number;
  video_path: string;
  video_size: string;
}

export interface ImageVideoObject {
  svid: string;
  filename: string;
  route: string;
  resource: any[];
  raw_width: string;
  raw_height: string;
  raw_rotate: string;
  img_urls: any[];
  bin_url: string;
  img_x_len: number;
  img_x_size: number;
  img_y_len: number;
  img_y_size: number;
}

export interface ImageTokenData {
  url: string;
  token: string;
}

export interface SearchResultData {
  list: SearchResultObject[];
  total_page: number;
  total_num: number;
  recommends: any[];
  similar: string;
  jump: null;
  se_id: string;
  banner: {
    icon: string;
    title: string;
    url: string;
  };
}

export interface SearchResultObject {
  id: number;
  title: string;
  org_title: string;
  alia_title: string[];
  horizontal_cover: string;
  square_cover: string;
  vertical_cover: string;
  author_name: string[];
  styles: string[];
  is_finish: number;
  allow_wait_free: boolean;
  discount_type: number;
  type: number;
  wiki: WikiObject;
  numbers: number;
}

export interface WikiObject {
  id: string;
  title: string;
  origin_title: string;
  vertical_cover: string;
  producer: string;
  author_name: string[];
  publish_time: string;
  frequency: string;
}
