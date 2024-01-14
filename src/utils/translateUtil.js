import axios from "axios";

export async function translate_conversations(lan_code, conversations) {
  const translate_to_lan_code = "en";
  const payload = {
    lan_code,
    conversations,
    translate_to_lan_code,
  };

  try {
    const response = await axios.post(
      `${process.env.VUE_APP_API_BASE_URL}/translate`,
      payload
    );
    return response.data;
  } catch (error) {
    console.log(error);
    throw error;
  }
}
