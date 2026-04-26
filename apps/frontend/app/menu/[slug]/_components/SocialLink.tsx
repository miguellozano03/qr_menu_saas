import { LinkType } from "@/lib/types/menu/menu";
import {
  FaInstagram,
  FaFacebook,
  FaTiktok,
  FaYoutube,
  FaWhatsapp,
  FaXTwitter,
} from "react-icons/fa6";
import { Globe } from "lucide-react";
import React from "react";

export const ICON_MAP: Record<LinkType, React.ReactNode> = {
  instagram: <FaInstagram />,
  facebook: <FaFacebook />,
  tiktok: <FaTiktok />,
  youtube: <FaYoutube />,
  whatsapp: <FaWhatsapp />,
  twitter: <FaXTwitter />,
  webiste: <Globe />,
  other: <Globe />,
};
